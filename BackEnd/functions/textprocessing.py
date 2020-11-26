import re
import string
import spacy
import numpy as np

from typing import Tuple, List
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import WordNetLemmatizer
from pathlib import Path

try:
    from collections.abc import Counter, OrderedDict
except ImportError:
    from collections import Counter, OrderedDict


class TextProcessor:

    def __init__(self):
        self.stop_words = set()
        with open(Path(__file__).parent.parent.parent / 'Data' / 'stopwords.txt') as f:
            lines = f.readlines()
            for line in lines:
                self.stop_words.add(line.rstrip())


    # Maddy
    # returns presence of tags in returned text, to be removed from main body
    @staticmethod
    def tag_visible(texts) -> bool:
        if texts.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(texts, Comment):
            return False
        return True

    # method for taking a string in HTML format and returning a string of the main body
    def extract_main_body_from_html(self, html_string: str) -> Tuple[str, str]:
        soup = BeautifulSoup(html_string, "html.parser")
        texts = soup.findAll(text=True)
        title = soup.find("title")
        visible_texts = filter(self.tag_visible, texts)
        body = u" ".join(t.string.strip() for t in visible_texts)
        if title is None:
            return "None", body
        else:
            return str(title.text), body

    # Alex Ll
    # Method for extracting all of the useful URLs from a HTML document
    @staticmethod
    def extract_urls_from_html(html_string: str) -> [str]:
        # list of valid urls to be returned
        valid_urls = []

        # setting up beautiful soup parser and scraping <a> tags
        soup = BeautifulSoup(html_string, 'html.parser')
        tags = soup.find_all('a')

        # scraping url links from <a> tags
        for url_link in tags:
            url_new = url_link.get('href')
            flag = False

            # checking if url already exists in return list
            for item in valid_urls:
                if url_new == item:
                    flag = True

            # checking if url is not empty and starts with 'http'
            if (url_new is not None) and (flag is False) and (str(url_new).startswith('http')):
                # append valid url to return list
                valid_urls.append(url_new)

        return valid_urls

    # Clean tweet text by removing links, special characters
    @staticmethod
    def clean_tweet(tweet: str) -> str:
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    @staticmethod
    def remove_emoji(location):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' ', location).strip()

    @staticmethod
    def clean_location(location,  countries, country_abbreviations, states, state_abbreviations) -> str:
        if location is None:
            return ""

        clean_location = TextProcessor.remove_emoji(location)

        punctuation = string.punctuation.replace(',', '')
        punctuation += "1234567890"
        if len(clean_location.split(' ')) < 4 and not any(elem in clean_location for elem in punctuation):
            clean_location = clean_location.lower().strip()

            if ',' in clean_location:
                place = clean_location.split(',')[1].strip()
                if any(map(place.__contains__, states)) or any(map(place.__contains__, countries)):
                    return clean_location
                else:
                    for word in clean_location.split(" "):
                        if word in state_abbreviations or word in country_abbreviations:
                            return clean_location
            else:
                if clean_location in countries or clean_location == "united states":
                    return clean_location

        return ""

    # method for taking an input string a return all the tokens
    @staticmethod
    def create_tokens_from_text(text: str) -> [str]:
        return re.findall(r"[\w']+|[.,!?;]", text)

    # method for taking a list of tokens and cleaning them. This involves removing punctuation,
    # stop word, making lower case, removing pure digit tokens, and stemming
    def clean_tokens(self, tokens: [str]) -> [str]:
        # removing all punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [t.translate(table) for t in tokens if t]

        # removing empty tokens
        stripped = list(filter(None, stripped))

        # make all tokens lower case
        stripped = list(map(lambda x: x.lower(), stripped))

        # removing all stop words
        stop_words = self.stop_words
        stripped = [s for s in stripped if s not in stop_words]

        # removing all tokens that are just digits
        stripped = [s for s in stripped if not re.search(r'\d', s)]

        # lemmatizing the remaining tokens
        lemmatizer = WordNetLemmatizer()
        stripped = [lemmatizer.lemmatize(token) for token in stripped]

        return stripped

    @staticmethod
    def calculate_key_words(tokens: [str], number_of_key_words: int) -> [str]:
        c = Counter(tokens)
        ordered_terms = list(c.keys())
        return ordered_terms[:number_of_key_words]

    # method altered from https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0
    def calculate_keywords_with_text_rank(self, text, number_of_keywords=10) -> List[Tuple[str, float]]:
        word_types = ['NOUN', 'PROPN']

        document = spacy.load('en_core_web_sm')(text)

        # make the sentences from the input text using spacy
        sentences = [[token.text.lower() for token in sent if token.pos_ in word_types and
                      token.text not in self.stop_words and token.text not in string.punctuation and len(token) > 1]
                     for sent in document.sents]
        sentences = list(filter(None, sentences))

        # generate a vocabulary of the text
        vocab = OrderedDict()
        i = 0
        words = set([w for sentence in sentences for w in sentence])
        for word in words:
            vocab[word] = i
            i += 1

        token_pairs = TextProcessor.get_token_pairs(4, sentences)

        normal_matrix = TextProcessor.get_matrix(vocab, token_pairs)
        weight_matrix = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(10):
            weight_matrix = (1 - 0.85) + 0.85 * np.dot(normal_matrix, weight_matrix)
            if abs(previous_pr - sum(weight_matrix)) < 1e-5:
                break
            else:
                previous_pr = sum(weight_matrix)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = weight_matrix[index]

        word_ranking = OrderedDict(sorted(node_weight.items(), key=lambda t: t[1], reverse=True))
        return [(key, value) for key, value in list(word_ranking.items())[:number_of_keywords]]

    # method taken from: https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0
    @staticmethod
    def get_token_pairs(window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    # method taken from: https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0
    @staticmethod
    def get_matrix(vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = g + g.T - np.diag(g.diagonal())

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm
