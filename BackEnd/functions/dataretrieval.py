import concurrent.futures
import concurrent.futures
import concurrent.futures
import csv
import json
import re
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Dict
from urllib.parse import urldefrag, urlparse
from tika import parser
import requests
import requests.exceptions
import tweepy
from googlesearch import search
from readability import Document
from requests import Response
from trafilatura import extract

from .analysis import NLP_Analyser
from .textprocessing import TextProcessor

MAX_THREADS = 50


# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        with open(Path(__file__).parent.parent.parent / 'Data' / 'blacklist.txt') as f:
            regexes = []
            lines = f.readlines()
            for line in lines:
                regexes.append(line.rstrip())
            self.BLACKLIST_REGEX = '(?:%s)' % '|'.join(regexes)
        pass

    def url_cleaner(self, urls: [str]) -> [str]:
        parent = []
        url_depth = []
        for url in urls:
            if not re.match(self.BLACKLIST_REGEX, url):
                link = urlparse(url)
                net = link.netloc
                if net not in parent:
                    parent.append(net)
                    url_depth.append(url)
        return url_depth

    # Maddy
    # not sure how we want to use this method yet
    def crawl_google_with_key_words(self, key_words: [str], urls_returned: int) -> [str]:
        query = ' '.join(key_words)
        google_result = search(query, tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned, pause=1)
        new_results = set()
        for url in google_result:
            if not re.match(self.BLACKLIST_REGEX, url):
                defrag_url = urldefrag(url)[0]
                new_results.add(defrag_url)
        return new_results

    # Alex Ll
    # recursively crawl a set of URLs with batch checking similarities
    def recursive_url_crawl(self, urls: [str], max_depth: int) -> dict:
        scraper = Scraper()
        final_dict = {}

        # for every base url
        url_depth = [[] for _ in range(0, max_depth + 1)]
        for url in urls:
            # Create list of searched URL's for use by the program
            url_depth[0].append(url)
        # Loop through all URLs in url_depth
        for depth_index in range(0, max_depth):
            urls = url_depth[depth_index]
            if len(urls) == 0:
                break
            start_t = datetime.now()

            print("Depth", depth_index)
            print("Batch Scraping", len(urls), "links: ")
            response = scraper.downloads(urls)
            print("Batch Scraping Complete.", len(response), "Links Scraped. Time Taken: ", datetime.now() - start_t)
            for k in response.keys():
                data = response[k]
                new_links = data.html_links
                for url_new in new_links:
                    # if link empty, continue
                    if url_new is None:
                        continue
                    flag = False  # Flag is true if website has been searched before
                    parsed_url = urlparse(url_new)
                    new_link = parsed_url.netloc + parsed_url.path

                    # Check to see if website has been visited before
                    if new_link in final_dict.keys():
                        flag = True
                    else:
                        for item in url_depth:
                            parsed_check_urls = [urlparse(x) for x in item]
                            new_parsed_links = [x.netloc + x.path for x in parsed_check_urls]
                            parent = [x.netloc for x in parsed_check_urls]
                            if len(parent) > 0:
                                if parsed_url.netloc in parent:
                                    flag = True
                                    break
                            elif new_link in new_parsed_links:
                                flag = True
                                break

                    if flag is False:
                        if not re.match(self.BLACKLIST_REGEX, url_new):
                            # Append url to search list, will be searched next
                            url_depth[depth_index + 1].append(url_new)
            final_dict.update(response)
        return final_dict

    @staticmethod
    def twitter_init():
        with open(Path(__file__).parent.parent.parent / 'Data' / "twitter_credentials.json", "r") as file:
            creds = json.load(file)

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    @staticmethod
    def location_lists_init():
        with open(Path(__file__).parent.parent.parent / 'Data' / 'countries.txt', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            data = list(reader)

        countries = []
        country_abbreviations = []

        for line in data:
            country = line[0]
            bracket_location = country.index('(')
            countries.append(country[:bracket_location - 1].strip().lower())
            country_abbreviations.append(country[bracket_location - 1:].strip("").lower()[2:4])

        country_abbreviations.sort()

        with open(Path(__file__).parent.parent.parent / 'Data' / 'states.txt', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            data = list(reader)

        states = []
        state_abbreviations = []
        for line in data:
            states.append(line[0].split("-")[0].strip().lower())
            state_abbreviations.append(line[0].split("-")[1].strip().lower())

        return countries, country_abbreviations, states, state_abbreviations

    def twitter_crawl(self, uid: str, keywords: [str], tweets_returned: int):
        api = self.twitter_init()
        # Retrieves all tweets with given keywords and count
        query = ' '.join(keywords[:2])
        searched_tweets = tweepy.Cursor(api.search, q="vaccine forced", result_type='popular').items(40)
        print("searched tweets:", searched_tweets)
        countries, country_abbreviations, states, state_abbreviations = self.location_lists_init()
        tweets = []
        for tweet in searched_tweets:
            print("tweet", tweet)
            parsed_tweet = {'uid': uid,
                            'created_at': tweet.created_at,
                            'text': tweet.text,
                            'favorite_count': tweet.favorite_count,
                            'retweet_count': tweet.retweet_count,
                            'user_location': TextProcessor.clean_location(tweet.user.location,
                                                                          countries, country_abbreviations,
                                                                          states, state_abbreviations),
                            'sentiment': NLP_Analyser.get_tweet_sentiment(tweet.text)}
            print("parsed tweet: ", parsed_tweet)
            tweets.append(parsed_tweet)
        print("number of tweets:", len(tweets))
        return tweets


Data = namedtuple('Data', 'uid content_type url raw_html title text_body cleaned_tokens html_links')


class Scraper:
    def __init__(self):
        self.lock = Lock()
        self.processor = TextProcessor()

    def downloads(self, urls: [str]) -> Dict[str, Data]:
        responses = {}
        threads = min(MAX_THREADS, len(urls))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            result = executor.map(self.scrape_url, urls)
        for r in result:
            url = r[0]
            data = r[1]
            if data is not None:
                responses[url] = data
        return responses

    # Alex Ll
    # method that returns all the HTML data from a URL
    def scrape_url(self, url: str) -> (str, Data):
        data = None
        try:
            request_resp = requests.get(url, allow_redirects=False, timeout=5)
            data = self.get_data_from_source(url, request_resp)
        except Exception as e:
            print("Exception:", e)
            pass

        return url, data

    # method for getting raw text and cleaned tokens from a source, can be a html or pdf
    def get_data_from_source(self, source: str, response: Response, seen_urls=None) -> namedtuple:
        # if seen_urls is default, set as an empty list to begin with
        if seen_urls is None:
            seen_urls = []

        print("Processing:", source)

        # if there is no response, no point in processing further
        if response is None:
            return None

        initial_html = ''
        title = ''
        url_regex = r"(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(?:[-a-zA-Z0-9(" \
                    r")@:%_\+.~#?&//=]*))"

        # if content-type is not in the headers, we won't be able to decipher if it is pdf or html, so skip
        if 'content-type' not in response.headers.keys():
            return None

        content_type = response.headers['content-type']

        # if the two MIME types we are looking for aren't present, return None to indicate no data
        if "application/pdf" not in content_type and "text/html" not in content_type:
            print(source, "failed content type check", content_type)
            return None

        # scraping stage
        # if the content is a pdf
        if "application/pdf" in content_type:
            content_type = "application/pdf"

            # get the content and process it through Apache Tika
            raw = response.content

            self.lock.acquire()
            try:
                processed_text = parser.from_buffer(raw)['content']
            finally:
                self.lock.release()

            # if we get a processed pdf out, get the make text and collect the urls from the text
            if processed_text is not None:
                main_text = ' '.join(processed_text.split())
                urls = re.findall(url_regex, main_text)
            else:
                return None
        # if the content is html
        else:
            content_type = "text/html"

            # get the base html out from the page
            initial_html = response.text

            # if there is no html, no point continuing with processing
            if initial_html is None or initial_html == "":
                return None

            # if there is a location header, we have to handle redirects
            if 'location' in response.headers.keys():
                location = response.headers['location']
                print("Seen URLs Length", len(seen_urls))

                # check if we have seen this url before
                if location in seen_urls:
                    print(source, "failed recursive location check")
                    return None

                # add to list of previously seen urls
                seen_urls.append(location)

                # try to get a new request from the redirected location
                try:
                    new_request_resp = requests.get(location, allow_redirects=False, timeout=5)
                except requests.exceptions.ConnectionError:
                    return None

                # recursively call the get_data_from_source function with the new request and new seen urls list
                return self.get_data_from_source(location, new_request_resp, seen_urls)

            # use readability-lxml to extract a list of urls
            url_doc = Document(initial_html).summary()

            # use trafilatura in order to extract the contents of the page
            try:
                doc = extract(initial_html, source, json_output=True)
            except TypeError:
                print(source, "produced type error")
                return None

            # if no document extracted, no point continuing
            if doc is None:
                print(source, "failed extraction")
                return None

            # create a dictionary from the json object returned
            article = json.loads(doc)

            # get the title and main text out of the article
            title = article['title']
            main_text = article['text'].rstrip()

            # if no main text, no point continuing
            if main_text is None:
                print(source, "failed plain text check")
                return None

            # collect the urls from the html extracted by readability-lxml
            urls = self.processor.extract_urls_from_html(url_doc)

        # make the tokens from the main text, and create a clean form
        tokens = TextProcessor.create_tokens_from_text(main_text)
        cleaned_tokens = self.processor.clean_tokens(tokens)

        return Data(uid="", content_type=content_type, url=source, raw_html=initial_html, title=title,
                    text_body=main_text, cleaned_tokens=cleaned_tokens, html_links=urls)
