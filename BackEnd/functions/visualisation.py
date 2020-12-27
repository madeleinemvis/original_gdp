from .textprocessing import TextProcessor
from .dbmanager import DbManager
from collections import Counter


# class for the data visualisation
class DataVisualiser:
    db_manager = None
    text_processor = None

    def __init__(self):
        self.db_manager = DbManager()
        self.text_processor = TextProcessor()

    # Returns a list of 20 common words that appeared throughout the texts
    def word_cloud(self, uid: str):
        # Get all keywords from mongodb (big big string) need UID
        # use TextProcessor method get_all_keywords_with_textrank we want approx 25 words
        text = self.db_manager.get_all_main_texts(uid)
        keywords_with_values = self.text_processor.calculate_keywords_with_text_rank(text, 25)
        return dict(keywords_with_values)

    def get_document_frequency(self, uid: str):
        count = self.db_manager.count_all_documents(uid)
        return count

    def get_tweet_frequency(self, uid: str):
        count = self.db_manager.count_all_tweets(uid)
        return count

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

    def get_sentiment_pie_chart(self, uid: str):
        tweets = self.db_manager.get_all_tweets(uid)
        c = Counter(tweets['sentiment'])
        c = dict(c)
        print("$$$ Pie Chart sentiment counts:", c)
        return c
