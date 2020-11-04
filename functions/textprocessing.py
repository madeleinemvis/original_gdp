import re
import string
from collections import Counter

from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextProcessor:

    def __init__(self):
        pass

    # Maddy
    # returns presence of tags in returned text, to be removed from main body
    def tag_visible(self, texts) -> bool:
        if texts.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(texts, Comment):
            return False
        return True

    # method for taking a string in HTML format and returning a string of the main body
    def extract_main_body_from_html(self, html_string: str) -> str:
        soup = BeautifulSoup(html_string, "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        body = u" ".join(t.string.strip() for t in visible_texts)
        return body

    # Maddy
    # method for creating a list of strings of meta data from a string in HTML format. 
    # Could make the output its own class for ease going forward
    def extract_meta_data_from_HTML(self, html_string: str) -> [str]:
        return []

    # Alex Ll
    # Method for extracting all of the useful URLs from a HTML document
    def extract_urls_from_html(self, html_string: str) -> [str]:
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
    def clean_tweet(self, tweet:str) -> str:
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    # method for taking an input string a return all the tokens
    def create_tokens_from_text(self, text: str) -> [str]:
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
        stop_words = set(stopwords.words('english'))
        stripped = [s for s in stripped if not s in stop_words]

        # removing all tokens that are just digits
        stripped = [s for s in stripped if not re.search(r'\d', s)]

        # stemming the remaining tokens
        porter = PorterStemmer()
        stripped = [porter.stem(token) for token in stripped]

        return stripped

    def calculate_key_words(self, clean_tokens: [str], number_of_key_words: int) -> [str]:
        c = Counter(clean_tokens)
        ordered_terms = list(c.keys())
        return ordered_terms[:number_of_key_words]
