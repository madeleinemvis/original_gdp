import json
import requests
import pandas as pd
from googlesearch import search
import requests.exceptions
import tweepy


# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        pass

    @staticmethod
    def crawl_google_with_key_words(key_words: [str], urls_returned: int) -> [str]:
        google_result = search(str(key_words), tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned, pause=2.0)
        return google_result

    # recursively crawl a set of URLs with batch checking similarities
    @staticmethod
    def recursive_url_crawl(urls: [str], max_depth: int) -> [str]:
        return []

    @staticmethod
    def twitter_init():
        with open("../twitter_credentials.json", "r") as file:
            creds = json.load(file)

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def twitter_crawl(self, key_words: [str], tweets_returned: int):
        api = self.twitter_init()
        # Retrieves all tweets with given keywords and count
        tweets = tweepy.Cursor(api.search, q=key_words).items(tweets_returned)
        # Loops through tweets and retrieves data
        tweet_list = [[tweet.id, tweet.created_at, tweet.text, tweet.favorite_count, tweet.entities['hashtags'],
                       tweet.user.location.encode('utf8')] for tweet in tweets]
        # Stores data into dataframe, may make it easier to store into DB
        tweets_df = pd.DataFrame(tweet_list, columns=['created_at', 'text', 'favorite_count', 'hashtags',
                                                      'user_location'])
        return tweets_df.to_json()


class Scraper:
    def __init__(self):
        pass

    # Alex Ll
    # method that returns all the HTML data from a URL
    @staticmethod
    def scrape_url(url: str) -> str:
        request = requests.get(url)
        return request.text
