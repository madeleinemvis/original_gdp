import pytest
from functions.textprocessing import TextProcessor


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

# TODO test location cleaning
