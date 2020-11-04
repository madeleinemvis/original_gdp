# class for doing all the NLP analysis needed
from functions.textprocessing import TextProcessor
from textblob import TextBlob


class NLP_Analyser:

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(TextProcessor.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
