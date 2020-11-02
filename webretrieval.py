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

    # Maddy
    # not sure how we want to use this method yet
    def crawl_google_with_key_words(self, key_words: [str], urls_returned: int) -> [str]:
        return search(key_words, tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned, pause=1.0)

    # Alex Ll
    # recursively crawl a set of URLs with batch checking similarities
    def recursive_url_crawl(self, urls: [str], max_depth: int) -> [str]:
        return []

    def twitter_init(self):
        with open("twitter_credentials.json", "r") as file:
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
        tweets_df = pd.DataFrame(tweet_list, columns=['tweet_id', 'created_at', 'text', 'favorite_count', 'hashtags',
                                                      'user_location'])
        return tweets_df.to_json()


class Scraper:
    def __init__(self):
        pass

    # Alex Ll
    # method that returns all the HTML data from a URL
    def scrape_url(self, URL: str) -> str:
        request = requests.get(URL)
        return request.text
