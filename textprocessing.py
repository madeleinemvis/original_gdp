from typing import TypedDict
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
import re, string

class TextProcessor:
    
    def __init__(self):
        pass

    # Maddy
    # method for taking a string in HTML format and returning a string of the main body
    def extract_main_body_from_HTML(html_string: str) -> str:
        pass

    # Maddy
    # method for creating a dictionary of meta data from a string in HTML format. 
    # Could make the dictionary its own class for ease going forward
    def extract_meta_data_from_HTML(html_string: str) -> TypedDict:
        pass

    # method for taking an input string a return all the tokens
    def create_tokens_from_text(text: str) -> [str]:
        return re.findall(r"[\w']+|[.,!?;]", text)

    # method for taking a list of tokens and cleaning them. This involves removing punctuation,
    # stop word, making lower case, removing pure digit tokens, and stemming
    def clean_tokens(tokens: [str]) -> [str]:
        # removing all punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [t.translate(table) for t in tokens if t]

        # removing empty tokens
        stripped = list(filter(None, stripped))

        # make all tokens lower case
        stripped = list(map(lambda x : x.lower(), stripped))

        # removing all stop words
        stop_words = set(stopwords.words('english'))
        stripped = [s for s in stripped if not s in stop_words]

        # removing all tokens that are just digits
        stripped = [s for s in stripped if not re.search(r'\d',s)]

        # stemming the remaining tokens
        porter = PorterStemmer()
        words = [porter.stem(word) for word in words]
        
    def calculate_key_words(clean_tokens: [str], number_of_key_words: int) -> [str]:
        c = Counter(clean_tokens)
        return c.keys()[:number_of_key_words]

        
