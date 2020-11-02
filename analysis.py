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


class NLP_Analyser:
    def __init__(self):
        with open('stopwords.txt') as f:
            stopwords = set()
            lines = f.readlines()
            for line in lines:
                stopwords.add(line.rstrip())
            self.stopwords = stopwords
        pass

    # Alex Lockwood
    # Method that creates the topic model from a list of documents
    # Assumed that the documents have not been cleaned - will be cleaned as a result
    def create_topic_model(self, documents):
        cleaned_documents = [
            gensim.utils.simple_preprocess(doc) for doc in documents]

        # Build the bigram and trigram models
        bigram = gensim.models.Phrases(
            cleaned_documents, min_count=5, threshold=100)
        trigram = gensim.models.Phrases(
            bigram[cleaned_documents], threshold=100)

        # Faster way to get a sentence clubbed as a bi or trigram
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        docs_nostops = self.__remove_stopwords(cleaned_documents)
        docs_bigrams = self.__make_bigrams(docs_nostops, bigram_mod)
        docs_lemmatised = self.__lemmatise(docs_bigrams)

        id2word = corpora.Dictionary(docs_lemmatised)
        corpus = [id2word.doc2bow(doc) for doc in docs_lemmatised]
        self.lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                         id2word=id2word,
                                                         num_topics=10,
                                                         random_state=100)

        self.docs_topics = [self.lda_model.get_document_topics(
            doc, minimum_probability=0) for doc in corpus]

    def __remove_stopwords(self, documents):
        return [[word for word in document if word not in self.stopwords] for document in documents]

    def __make_bigrams(self, documents, bigram_mod):
        return [bigram_mod[document] for document in documents]

    def __make_trigrams(self, documents, bigram_mod, trigram_mod):
        return [trigram_mod[bigram_mod[document]] for document in documents]

    def __lemmatise(self, documents, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        nlp = spacy.load('en', disable=['parser', 'ner'])
        texts_out = []
        for document in documents:
            doc = nlp(" ".join(document))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out
