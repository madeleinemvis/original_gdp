import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.matutils import cossim
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

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
