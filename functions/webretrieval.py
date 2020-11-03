import json
import requests
import pandas as pd
from googlesearch import search
import requests.exceptions
import tweepy
from bs4 import BeautifulSoup
import requests
import re


# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        pass

    # Maddy
    # not sure how we want to use this method yet
    def crawl_google_with_key_words(self, key_words: [str], urls_returned: int) -> [str]:
        google_result = search(str(key_words), tld="com", lang="en", num=urls_returned, start=0, stop=urls_returned, pause=2.0)
        return google_result

    # Alex Ll
    # recursively crawl a set of URLs with batch checking similarities
    def recursive_url_crawl(self, urls: [str], max_depth: int) -> [str]:
        scraper = Scraper()
        final_list = []
        for url in urls:
            # Create list of searched URL's for use by the program
            url_depth = [[] for i in range(0, max_depth + 1)]
            url_depth[0].append(url)
            loop = []
            
            # Loop through all URL's in url_depth
            for depth_index in range(0, max_depth):
                for web_links in url_depth[depth_index]:
                    
                    # Process crawl response
                    response = scraper.scrape_url(web_links)
                    soup = BeautifulSoup(response, 'html.parser')
                    tags = soup.find_all('a')
                    
                    # Loop through web links found in response
                    for url_link in tags:
                        url_new = url_link.get('href')
                        flag = False # Flag is true if website has been searched before
                        
                        # Check to see if website has been visited before
                        for item in url_depth:
                            for i in item:
                                if url_new == i:
                                    flag = True
                        
                        # If link is not empty and has not been searched before
                        if url_new is not None and flag is False:
                            
                            # If link is a valid url
                            if str(url_new).startswith('http'):
                                old_link = web_links.rsplit('.', 1)[0]
                                new_link = str(url_new).rsplit('.', 1)[0]
                                
                                # Check to see if current link is not from the same website that current link was pulled from
                                if not re.search(old_link, new_link):
                                    
                                    # Append url to search list, will be searched next
                                    url_depth[depth_index + 1].append(url_new)
                                    
                                    # Append to list of valid sites pulled from parent site
                                    loop.append(url_new)
            
            # Append loop list to final return list
            final_list.append(loop)
        return final_list

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
        try:
            request = requests.get(URL)
        except requests.ConnectionError:
            print('---Connection Error---')
            return ''
        return request.text
