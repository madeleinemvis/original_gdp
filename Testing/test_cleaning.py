import pytest
from BackEnd.functions.textprocessing import TextProcessor
from BackEnd.functions.dataretrieval import Crawler


@pytest.mark.parametrize("raw_location, clean_location", [
    ("London", "London"),
    ("the coven 📍", "the coven"),
    ("Tucson Arizona🌵☀️", "Tucson Arizona"),
    ("🍔", ""),
    ("Albany, New York 👀", "Albany, New York"),
    ("harlem❤charlit❤detroit❤paisley park💙mommy", "harlem charlit detroit paisley park mommy")
])
def test_emoji_cleaning(raw_location, clean_location):
    assert TextProcessor.remove_emoji(raw_location) == clean_location.strip()


@pytest.mark.parametrize("raw_string, tokens", [
    ("absolute", "absolute".split(" ")),
    ("a short sentence", "a short sentence".split(" ")),
    ("some! punctuation-has, been # put here", "some ! punctuation has , been put here".split(" "))
])
def test_tokenization(raw_string, tokens):
    assert TextProcessor.create_tokens_from_text(raw_string) == tokens


@pytest.fixture
def location_lists():
    return Crawler.location_lists_init()


@pytest.mark.parametrize("raw_string, location", [
    ("London", ""),
    ("EN", ""),
    ("Egypt", "egypt"),
    ("12 France", ""),
    ("orlando, FlorIdA", "orlando, florida"),
    ("#NYC", ""),
    ("USA", ""),
    ("Nottingham, eN", "nottingham, en"),
    ("IA, USA", "ia, usa"),
    ("Islamabad, Pakistan", "islamabad, pakistan"),
    ("St. Helena", "st. helena"),
    ("somalia slovenia slovakia serbia spain", ""),
    ("Oman!", "")
    ])
def test_location_cleaning(raw_string, location, location_lists):
    assert TextProcessor.clean_location(raw_string, location_lists[0], location_lists[1], location_lists[2], location_lists[3]) == location


# TODO Maddy
@pytest.mark.parametrize("raw_tweet, clean_tweet", [
    ("example https://www.google.com", "example"),
    ("", "")
    ])
def test_twitter_cleaning(raw_tweet, clean_tweet):
    assert TextProcessor.clean_tweet(raw_tweet) == clean_tweet
