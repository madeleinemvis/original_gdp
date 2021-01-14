# Adapted from @amazingclaude/Fake_News_Stance_Detection

import nltk
import re
from nltk.corpus import stopwords

_wnl = nltk.WordNetLemmatizer()


def normalize_word(w):
    return _wnl.lemmatize(w).lower()


def get_tokenized_lemmas(s):
    return [normalize_word(t) for t in nltk.word_tokenize(s)]


# this clean function is used for term frequency calculating,
# therefore question mark & short words (like not, no) are considered.
def clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric
    cleaned_text = " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()
    # get rid of the nummbers
    cleaned_text = re.sub(r'\d+', '', cleaned_text, flags=re.UNICODE)
    # find out the question mark
    question_mark = " ".join(re.findall(r'[?]\W', s, flags=re.UNICODE))
    # combine the question mark and the cleaned strings
    cleaned_text_with_question_mark = " ".join([cleaned_text, question_mark])
    # tokenize
    cleaned_text_with_lemma = get_tokenized_lemmas(cleaned_text_with_question_mark)
    return cleaned_text_with_lemma

