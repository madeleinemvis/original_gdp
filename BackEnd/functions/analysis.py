from pathlib import Path
from typing import Dict

import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from textblob import TextBlob

from textprocessing import TextProcessor


class NLPAnalyser:
    def __init__(self):
        self.id2word = None
        self.sim_model = None
        self.tf_idf = None

        with open(Path(__file__).parent.parent.parent / 'Data' / 'stopwords.txt') as f:
            stopwords = set()
            lines = f.readlines()
            for line in lines:
                stopwords.add(line.rstrip())
            self.stopwords = stopwords
        pass

    @staticmethod
    def get_tweet_sentiment(tweet: str) -> str:
        analysis = TextBlob(TextProcessor.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # Alex Lockwood
    # Method that creates the topic model from a list of documents
    # Assumed that the documents have not been cleaned - will be cleaned as a result
    def create_tfidf_model(self, scraped_data: Dict):
        cleaned_documents = [scraped_data[k].cleaned_tokens for k in scraped_data.keys() if scraped_data[k] is not None]
        self.id2word = corpora.Dictionary(cleaned_documents)
        corpus = [self.id2word.doc2bow(text) for text in cleaned_documents]
        self.tf_idf = gensim.models.TfidfModel(corpus)
        self.sim_model = gensim.similarities.SparseMatrixSimilarity(self.tf_idf[corpus],
                                                                    num_features=len(self.id2word))

    def check_similarity(self, document):
        if document is None:
            return 0
        cleaned_tokens = document.cleaned_tokens
        test_corpus = self.id2word.doc2bow(cleaned_tokens)
        return self.sim_model[test_corpus]
