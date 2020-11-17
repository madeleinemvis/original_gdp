from urllib.error import HTTPError

from functions.textprocessing import TextProcessor
from tika import parser  # Note this module needs Java to be installed on the system to work.
from functions.analysis import NLP_Analyser
from collections import namedtuple
from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests.exceptions
import tweepy
from urllib.parse import urlparse
import requests
from readabilipy import simple_json_from_html_string
import re
import csv
from pathlib import Path
from datetime import datetime


# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        with open('../blacklist.txt') as f:
            regexes = []
            lines = f.readlines()
            for line in lines:
                regexes.append(line.rstrip())
            self.BLACKLIST_REGEX = '(?:%s)' % '|'.join(regexes)
        pass

    # Maddy
    # not sure how we want to use this method yet
    def crawl_google_with_key_words(self, key_words: [str], urls_returned: int) -> [str]:
        query = ' '.join(key_words)
        google_result = search(query, tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned)
        new_results = []
        for url in google_result:
            if not re.match(self.BLACKLIST_REGEX, url):
                new_results.append(url)
        return new_results

    # Alex Ll
    # recursively crawl a set of URLs with batch checking similarities
    def recursive_url_crawl(self, urls: [str], max_depth: int) -> dict:
        scraper = Scraper()
        final_dict = {}

        # for every base url
        for url in urls:
            # Create list of searched URL's for use by the program
            url_depth = [[] for _ in range(0, max_depth + 1)]
            url_depth[0].append(url)
            loop = []

            # Loop through all URL's in url_depth
            for depth_index in range(0, max_depth):
                for web_links in url_depth[depth_index]:
                    # Process crawl response
                    data = scraper.get_data_from_source(web_links)
                    if data is not None:
                        tags = data.html_links
                        final_dict[web_links] = data

                        # Loop through web links found in response
                        for url_new in tags:
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
                                    if new_link in new_parsed_links:
                                        flag = True
                                        break

                            # If link is not empty and has not been searched before
                            if url_new is not None and flag is False:
                                # If link is a valid url
                                if str(url_new).startswith('http'):
                                    # If the link is not blacklisted
                                    if not re.match(self.BLACKLIST_REGEX, url_new):
                                        # Append url to search list, will be searched next
                                        url_depth[depth_index + 1].append(url_new)

                                        # Append to list of valid sites pulled from parent site
                                        loop.append(url_new)
        return final_dict

    @staticmethod
    def twitter_init():
        with open("../twitter_credentials.json", "r") as file:
            creds = json.load(file)

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    @staticmethod
    def location_lists_init():
        path = Path(__file__).parent / "../Data/"

        with open(path / 'countries.txt', newline='', encoding='utf8') as f:
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

        with open(path / 'states.txt', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            data = list(reader)

        states = []
        state_abbreviations = []
        for line in data:
            states.append(line[0].split("-")[0].strip().lower())
            state_abbreviations.append(line[0].split("-")[1].strip().lower())

        return countries, country_abbreviations, states, state_abbreviations

    def twitter_crawl(self, keywords: [str], tweets_returned: int):
        api = self.twitter_init()
        # Retrieves all tweets with given keywords and count
        query = ' '.join(keywords)
        searched_tweets = tweepy.Cursor(api.search, q=query).items(tweets_returned)
        countries, country_abbreviations, states, state_abbreviations = self.location_lists_init()
        tweets = []

        for tweet in searched_tweets:
            parsed_tweet = {'created_at': tweet.created_at,
                            'text': tweet.text,
                            'favorite_count': tweet.favorite_count,
                            'retweet_count': tweet.retweet_count,
                            'user_location': TextProcessor.clean_location(tweet.user.location,
                                                                          countries, country_abbreviations,
                                                                          states, state_abbreviations),
                            'sentiment': NLP_Analyser.get_tweet_sentiment(tweet.text)}
            # print(parsed_tweet['user_location'] + "|" + parsed_tweet['text'])

            if tweet.retweet_count > 0:
                # Only appends if the tweet text is unique
                if not any(t['text'] == parsed_tweet['text'] for t in tweets):
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        return tweets


Data = namedtuple('Data', 'url raw_html title text_body tokens html_links')


class Scraper:
    def __init__(self):
        self.processor = TextProcessor()

    # method for getting raw text and cleaned tokens from a source, can be a html or '.pdf'
    def get_data_from_source(self, source: str, seen_urls=None) -> namedtuple:
        if seen_urls is None:
            seen_urls = []

        initial_html = ''
        title = ''
        url_regex = r"(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(?:[-a-zA-Z0-9(" \
                    r")@:%_\+.~#?&//=]*))"

        # request the contents of the URL and get the 'content-type' header
        try:
            request = requests.get(source)
        except HTTPError:
            return None
        content_type = request.headers['content-type']

        # if the two MIME types we are looking for aren't present, return None to indicate no data
        if "application/pdf" not in content_type and "text/html" not in content_type:
            return None

        # scraping stage
        start_t = datetime.now()
        if "application/pdf" in content_type:
            raw = request.content
            processed_text = parser.from_buffer(raw)['content']
            if processed_text is not None:
                main_text = ' '.join(processed_text.split())
                urls = re.findall(url_regex, main_text)
            else:
                return None
        else:
            if 'location' in request.headers.keys():
                if source in seen_urls:
                    return None
                new_seen_urls = seen_urls.append(source)
                print("Scraped: ", source, ". Time taken: ", datetime.now() - start_t)
                return self.get_data_from_source(request.headers['location'], new_seen_urls)
            initial_html = request.content.decode('utf-8', 'ignore')

            article = simple_json_from_html_string(initial_html, use_readability=True)
            title = article['title']
            main_text_unprocessed = article['plain_text']
            if main_text_unprocessed is None:
                return None
            main_text = ''
            for text in main_text_unprocessed:
                main_text += text['text'].replace("ï¿1⁄2", "'") + " "
            urls = self.processor.extract_urls_from_html(article['content'])
        print("Scraped: ", source, ". Time taken: ", datetime.now() - start_t)

        # make the tokens from the main text, and create a clean form
        tokens = TextProcessor.create_tokens_from_text(main_text)
        cleaned_tokens = TextProcessor.clean_tokens(tokens)

        return Data(url=source, raw_html=initial_html, title=title, text_body=main_text, tokens=cleaned_tokens,
                    html_links=urls)


if __name__ == "__main__":
    scraper = Scraper()
    print(scraper.get_data_from_source("https://www.theguardian.com/politics/2020/nov/13/dominic-cummings-has-already-left-job-at-no-10-reports").text_body)
