import pytest
from functions.dataretrieval import Crawler


# test loading blacklist.txt
def test_load_blacklist_txt():
    with open('../Data/blacklist.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 15


# test loading countries.txt
def test_load_countries_txt():
    with open('../Data/countries.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 252


# test loading states.txt
def test_load_states_txt():
    with open('../Data/states.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 50


# test loading stopwords.txt
def test_load_stopwords_txt():
    with open('../Data/stopwords.txt') as file:
        lines = file.readlines()
        assert len(lines) >= 665


# test loading countries.txt
def test_load_lists_loading():
    assert all([x is not None for x in Crawler.location_lists_init()])
