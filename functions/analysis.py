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
    def __init__(self):
        with open('stopwords.txt') as f:
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
    def create_topic_model(self, documents):
        cleaned_documents = [documents[key][3]
                             for key in documents.keys() if documents[key] is not None]

        # Build the bigram and trigram models
        bigram = gensim.models.Phrases(
            cleaned_documents, min_count=5, threshold=100)
        trigram = gensim.models.Phrases(
            bigram[cleaned_documents], threshold=100)

        # Faster way to get a sentence clubbed as a bi or trigram
        self.bigram_mod = gensim.models.phrases.Phraser(bigram)
        self.trigram_mod = gensim.models.phrases.Phraser(trigram)

        docs_nostops = self.__remove_stopwords(cleaned_documents)
        docs_bigrams = self.__make_bigrams(
            docs_nostops, self.bigram_mod)
        docs_lemmatised = self.__lemmatise(docs_bigrams)

        self.id2word = corpora.Dictionary(docs_lemmatised)
        self.corpus = [self.id2word.doc2bow(doc) for doc in docs_lemmatised]
        self.lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                                         id2word=self.id2word,
                                                         num_topics=10,
                                                         random_state=100)

        self.docs_topics = [self.lda_model.get_document_topics(
            doc, minimum_probability=0) for doc in self.corpus]

    def check_similarity(self, document):
        if document is None:
            return 0
        extracted_doc = [document[3]]

        doc_nostops = self.__remove_stopwords(extracted_doc)
        doc_bigrams = self.__make_bigrams(
            doc_nostops, self.bigram_mod)
        doc_lemmatised = self.__lemmatise(doc_bigrams)

        doc_bow = self.id2word.doc2bow(doc_lemmatised[0])
        doc_topics = self.lda_model.get_document_topics(
            doc_bow, minimum_probability=0)

        similarity = 0

        for model_doc_topics in self.docs_topics:
            similarity += cossim(model_doc_topics, doc_topics)

        similarity /= len(self.docs_topics)
        return similarity

    def __remove_stopwords(self, documents):
        return [[word for word in document if word not in self.stopwords] for document in documents]

    def __make_bigrams(self, documents, bigram_mod):
        return [bigram_mod[document] for document in documents]

    def __lemmatise(self, documents, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        nlp = spacy.load('en', disable=['parser', 'ner'])
        texts_out = []
        for document in documents:
            doc = nlp(" ".join(document))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out
>>>>>>> functions/analysis.py
