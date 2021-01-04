import json
from collections import Counter

import pandas as pd

from BackEnd.functions.dbmanager import DbManager
from BackEnd.functions.textprocessing import TextProcessor


# class for the data visualisation
# Each function returns data formatted for a particular visual on the dashboard.
# All visuals are processed in this class
class DataVisualiser:
    db_manager = None
    text_processor = None

    def __init__(self):
        self.db_manager = DbManager()
        self.text_processor = TextProcessor()

    # Returns a list of 25 most common words that appeared throughout the texts
    def word_cloud(self, uid: str):
        # Get all keywords from mongodb (big big string) need UID
        # use TextProcessor method calculate_key_words
        tokens = self.db_manager.get_all_cleaned_tokens(uid)
        keywords_with_values = self.text_processor.calculate_key_words(tokens, 25)
        return dict(keywords_with_values)

    # Returns the number of documents that have been stored under the specified UID
    def get_document_frequency(self, uid: str):
        count = self.db_manager.count_all_documents(uid)
        return count

    # Returns the number of tweets that have been stored under the specified UID
    def get_tweet_frequency(self, uid: str):
        count = self.db_manager.count_all_tweets(uid)
        return count

    # Returns a dictionary of the number of tests passed for the econ, health and politics causal analysis
    def get_causal_gauge(self, uid: str):
        c = self.db_manager.get_causal(uid)
        causal = dict({'econ': c['econ_count'], 'health': c['health_count'], 'politics': c['politics_count']})
        return causal

    # Returns a dictionary of countries and their respective trend value from the causal data
    def get_trend_map(self, uid: str):
        c = self.db_manager.get_causal(uid)
        countries = json.loads(c['map_countries'])
        trends = json.loads(c['map_trends'])
        causal = dict({'countries': countries, 'trends': trends})
        return causal

    # Returns a dictionary of all causal data for each sector for the bar-graph visuals
    def get_causal_bar(self, uid: str):
        c = self.db_manager.get_causal(uid)
        causal = dict({'econ_estimate': c['econ_estimate'], 'econ_random': c['econ_random'],
                       'econ_unobserved': c['econ_unobserved'], 'econ_placebo': c['econ_placebo'],
                       'econ_subset': c['econ_subset'],
                       'health_estimate': c['health_estimate'], 'health_random': c['health_random'],
                       'health_unobserved': c['health_unobserved'], 'health_placebo': c['health_placebo'],
                       'health_subset': c['health_subset'],
                       'politics_estimate': c['politics_estimate'], 'politics_random': c['politics_random'],
                       'politics_unobserved': c['politics_unobserved'], 'politics_placebo': c['politics_placebo'],
                       'politics_subset': c['politics_subset'],
                       })
        return causal

    # Returns a list containing the Tweet's query, total favourites and total retweets, under a UID
    def get_tweet_summary(self, uid: str):
        tweets = self.db_manager.get_all_tweets(uid)
        t_query = self.db_manager.get_query(uid)
        favourites = 0
        retweets = 0
        no_of_tweets = len(tweets)
        for t in tweets:
            favourites += t['favorite_count']
            retweets += t['retweet_count']
        q = t_query
        q = q.replace('[', '')
        q = q.replace(']', '')
        q = q.replace('\'', '')
        q = q.replace(',', '')
        q = "\"" + q + "\""
        return [no_of_tweets, favourites, retweets, q]

    # Returns a dictionary of all Tweets retweets, favourites, separated by their sentiment, under a UID
    def get_sentiment_scatter(self, uid: str):
        tweets = self.db_manager.get_all_tweets(uid)
        positive = []
        neutral = []
        negative = []
        for t in tweets:
            if t['sentiment'] == 'negative':
                negative.append(dict({'y': t['retweet_count'], 'x': t['favorite_count']}))
            if t['sentiment'] == 'neutral':
                neutral.append(dict({'y': t['retweet_count'], 'x': t['favorite_count']}))
            elif t['sentiment'] == 'positive':
                positive.append(dict({'y': t['retweet_count'], 'x': t['favorite_count']}))

        return dict({'positive': positive, 'neutral': neutral, 'negative': negative})

    # Returns a dictionary with the counts of Tweet's sentiments under a UID
    def get_sentiment_pie_chart(self, uid: str):
        tweets = self.db_manager.get_all_tweets(uid)
        tweets_df = pd.DataFrame(tweets)
        c = Counter(tweets_df['sentiment'].tolist())
        c = dict(c)
        return c

    # Returns a list of dates of Tweets published, with their impact (sum of favourites & retweets for each day)
    def get_date_impact(self, uid: str):
        tweets = self.db_manager.get_all_tweets(uid)
        tweets_df = pd.DataFrame(tweets)
        tweets_df['date'] = tweets_df['created_at'].apply(lambda x: str(x.day) + "/" + str(x.month) + "/" + str(x.year))
        dates = sorted(tweets_df['date'].tolist(), key=lambda x: (int(x.split("/")[2]), int(x.split("/")[1]), int(x.split("/")[0])))
        impact = [sum(i) for i in zip(tweets_df['retweet_count'].tolist(), tweets_df['favorite_count'].tolist())]
        return [dates, impact]

    # Returns a list of dictionaries, representing the documents.
    def get_all_documents(self, uid: str):
        documents = self.db_manager.get_all_documents(uid)
        doc_list = []
        for d in documents:
            doc_list.append(dict({'title': d['title'], 'url': d['url'], 'sentiment': d['sentiment'],
                                  'stance': d['stance']}))
        return doc_list

    def get_website_graph(self, uid: str):
        graph = self.db_manager.get_website_graph(uid)
        return graph
