from .textprocessing import TextProcessor
from .dbmanager import DbManager
import json

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

    def get_causal_gauge(self, uid: str):
        c = self.db_manager.get_causal(uid)
        causal = dict({'econ': c['econ_count'], 'health': c['health_count'], 'politics': c['politics_count']})
        return causal
    
    def get_trend_map(self, uid: str):
        c = self.db_manager.get_causal(uid)
        countries = json.loads(c['map_countries'])
        trends = json.loads(c['map_trends'])
        causal = dict({'countries': countries, 'trends': trends})
        print(causal)
        return causal

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
