from pathlib import Path

from BackEnd.functions.dataretrieval import Crawler


# ALL TESTS WERE IMPLEMENTED DURING THE IMPLEMENTATION STAGE, ONCE WE IMPLEMENTED OUR APP WITH DJANGO
# THESE TESTS NO LONGER RUN SUCCESSFULLY

# test loading blacklist.txt
def test_load_blacklist_txt():
    with open('../Data/blacklist.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 15


# test loading countries.txt
def test_load_countries_txt():
    with open(Path(__file__).parent.parent / 'Data' / 'countries.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 252


# test loading states.txt
def test_load_states_txt():
    with open(Path(__file__).parent.parent / 'Data' / 'states.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 50


# test loading stopwords.txt
def test_load_stopwords_txt():
    with open(Path(__file__).parent.parent / 'Data' / 'stopwords.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 665


# test loading countries.txt
def test_load_location_lists_init():
    assert all([x is not None for x in Crawler.location_lists_init()])


def test_twitter_init():
    assert Crawler.twitter_init() is not None
