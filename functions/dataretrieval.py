from functions.textprocessing import TextProcessor
from tika import parser  # Note this module needs Java to be installed on the system to work.
from functions.analysis import NLP_Analyser
from collections import namedtuple
from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests.exceptions
import tweepy
import requests
import re
from datetime import datetime

from functions.analysis import NLP_Analyser
from functions.textprocessing import TextProcessor

THRESHOLD = 0.3

# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        pass

    # Maddy
    # not sure how we want to use this method yet
    @staticmethod
    def crawl_google_with_key_words(key_words: [str], urls_returned: int) -> [str]:
        query = ' '.join(key_words)
        google_result = search(query, tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned)
        return google_result

    # Alex Ll
    # recursively crawl a set of URLs with batch checking similarities
    @staticmethod
    def recursive_url_crawl(urls: [str], max_depth: int, analyser: NLP_Analyser) -> [str]:
        scraper = Scraper()
        processor = TextProcessor()
        final_list = []
        for url in urls:
            # Create list of searched URL's for use by the program
            url_depth = [[] for _ in range(0, max_depth + 1)]
            url_depth[0].append(url)
            loop = []

            # Loop through all URL's in url_depth
            for depth_index in range(0, max_depth):
                for web_links in url_depth[depth_index]:

                    # Get data for the link
                    data = scraper.get_data_from_source(web_links)

                    # If the similarity is less than the threshold, skip
                    if (analyser.check_similarity(data.tokens) < THRESHOLD):
                        continue

                    response = data.raw_html
                    soup = BeautifulSoup(response, 'html.parser')
                    tags = soup.find_all('a')

                    # Loop through web links found in response
                    for url_link in tags:
                        url_new = url_link.get('href')
                        flag = False  # Flag is true if website has been searched before


                        new_link = str(url_new).rsplit('.', 1)[0]
                        # Check to see if website has been visited before
                        for item in url_depth:
                            for i in item:
                                if url_new == i:
                                    flag = True
                                old_link = i.rsplit('.', 1)[0]
                                temp = old_link.rsplit('/', 1)
                                old1 = 'https://' + temp[1]
                                old2 = 'http://' + temp[1]
                                if re.search(old1, new_link) or re.search(old2, new_link):
                                    flag = True
                                
                                

                        # If link is not empty and has not been searched before
                        if url_new is not None and flag is False:

                            # If link is a valid url
                            if str(url_new).startswith('http'):
                                # Append url to search list, will be searched next
                                url_depth[depth_index + 1].append(url_new)

                                # Append to list of valid sites pulled from parent site
                                loop.append(url_new)

            # Append loop list to final return list
            final_list.append(loop)
        return final_list

    @staticmethod
    def twitter_init():
        with open("twitter_credentials.json", "r") as file:
            creds = json.load(file)

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    # TODO use keywords and tweet_returned rather than "vaccine autism" & 100
    def twitter_crawl(self, keywords: [str], tweets_returned: int):
        api = self.twitter_init()
        # Retrieves all tweets with given keywords and count
        searched_tweets = tweepy.Cursor(api.search, q="vaccine autism").items(tweets_returned)
        tweets = []
        for tweet in searched_tweets:
            parsed_tweet = {'created_at': tweet.created_at,
                            'text': tweet.text,
                            'favorite_count': tweet.favorite_count,
                            'retweet_count': tweet.retweet_count,
                            'user_location': TextProcessor.clean_location(tweet.user.location.encode('utf8')),
                            'sentiment': NLP_Analyser.get_tweet_sentiment(tweet.text)}

            if tweet.retweet_count > 0:
                # Only appends if the tweet text is unique
                if not any(t['text'] == parsed_tweet['text'] for t in tweets):
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        return tweets


Data = namedtuple('Data', 'url raw_html title text_body tokens html_links')


class Scraper:

    # Alex Ll
    # method that returns all the HTML data from a URL
    @staticmethod
    def scrape_url(url: str) -> str:
        try:
            start_t = datetime.now()
            request = requests.get(url)
            print("Scraped: ", url, ". Time taken: ", datetime.now() - start_t)
        except requests.ConnectionError:
            print('Connection Error: ' + url)
            return ''
        return request.text

    # method to get all of the text out of a pdf, but it does not clean it
    @staticmethod
    def scrape_pdf(pdf_path: str) -> str:
        start_t = datetime.now()
        raw = parser.from_file(pdf_path)
        raw_text = raw['content']
        print("Scraped: ", pdf_path, ". Time taken: ", datetime.now() - start_t)
        return ' '.join(raw_text.split())

    # method for getting raw text and cleaned tokens from a source, can be a html or '.pdf'
    @staticmethod
    def get_data_from_source(source: str) -> namedtuple:
        initial_html = ''
        title = ''
        if source.endswith('.pdf'):
            main_text = Scraper.scrape_pdf(source)
            # TODO get the urls links out of the pdf
            urls = []
        else:
            initial_html = Scraper.scrape_url(source)
            processor = TextProcessor()
            title, main_text = processor.extract_main_body_from_html(initial_html)
            urls = processor.extract_urls_from_html(initial_html)

        # make the tokens from the main text, and create a clean form
        tokens = TextProcessor.create_tokens_from_text(main_text)
        cleaned_tokens = TextProcessor.clean_tokens(tokens)

        return Data(url=source, raw_html=initial_html, title=title, text_body=main_text, tokens=cleaned_tokens,
                    html_links=urls)
