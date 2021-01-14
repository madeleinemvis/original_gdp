import pytest
from BackEnd.functions.textprocessing import TextProcessor
from BackEnd.functions.dataretrieval import Crawler

# ALL TESTS WERE IMPLEMENTED DURING THE IMPLEMENTATION STAGE, ONCE WE IMPLEMENTED OUR APP WITH DJANGO
# THESE TESTS NO LONGER RUN SUCCESSFULLY

@pytest.fixture
def get_processor():
    return TextProcessor()


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
    ("some! punctuation-has, been # put here", "some ! punctuation has , been put here".split(" ")),
    ("", []),
    ("123", "123".split(" ")),
    ("    ", []),
    ("The Vice President is also part of the Executive Branch, ready to assume the Presidency should the need arise.",
     "The Vice President is also part of the Executive Branch ,"
     " ready to assume the Presidency should the need arise .".split(" ")),
    ("The +Kingdom £of Engl@nd – which after 1535 included Wales"
     " – ceased being \"a\" separate$ sovereign @ state on (1) May 1707",
     "The Kingdom of Engl nd which after 1535 included Wales"
     " ceased being a separate sovereign state on 1 May 1707".split(" "))
])
def test_creating_tokens_from_text(raw_string, tokens):
    assert TextProcessor.create_tokens_from_text(raw_string) == tokens


@pytest.mark.parametrize("raw_tokens, clean_tokens", [
    (["absolute"], ["absolute"]),
    ("a short sentence".split(" "), "short sentence".split(" ")),
    ("some ! punctuation has , been put here ?".split(" "), "punctuation".split(" ")),
    ([], []),
    ("1 2 3 456".split(" "), []),
    ("    ".split(" "), []),
    ("The Vice President is also part of the Executive Branch ,"
     " ready to assume the Presidency should the need arise .".split(" "),
     "vice president executive branch ready assume presidency".split(" ")
     ),
    ("The Kingdom of Engl nd which after 1535 included Wales"
     " ceased being a separate sovereign state on 1 May 1707".split(" "),
     "kingdom engl included wale ceased separate sovereign state".split(" ")),
     (["\n"], []),
    (["\t \r \n     ".split(" ")], [])
])
def test_token_cleaning(get_processor, raw_tokens, clean_tokens):
    assert get_processor.clean_tokens(raw_tokens) == clean_tokens


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
