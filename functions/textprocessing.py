import re
import string
from collections import Counter
from typing import Tuple

from bs4 import BeautifulSoup
from bs4.element import Comment, PageElement
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TextProcessor:

    def __init__(self):
        pass

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
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    @staticmethod
    def clean_location(location) -> str:
        location = location.decode("utf-8")
        if len(location) == 0:
            return ""

        characters_to_remove = string.punctuation.replace(',', '') + "1234567890"

        if len(location.split(' ')) < 4 and not any(elem in location for elem in characters_to_remove):
            return location.lower()
        else:
            return ""

    # method for taking an input string a return all the tokens
    @staticmethod
    def create_tokens_from_text(text: str) -> [str]:
        return re.findall(r"[\w']+|[.,!?;]", text)

    # method for taking a list of tokens and cleaning them. This involves removing punctuation,
    # stop word, making lower case, removing pure digit tokens, and stemming
    @staticmethod
    def clean_tokens(tokens: [str]) -> [str]:
        # removing all punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [t.translate(table) for t in tokens if t]

        # removing empty tokens
        stripped = list(filter(None, stripped))

        # make all tokens lower case
        stripped = list(map(lambda x: x.lower(), stripped))

        # removing all stop words
        stop_words = set(stopwords.words('english'))
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
