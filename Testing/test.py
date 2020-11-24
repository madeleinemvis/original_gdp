import pytest
from functions.textprocessing import TextProcessor
from functions.dataretrieval import Scraper, Crawler
import time


@pytest.fixture
def get_scraper():
    return Scraper()


@pytest.fixture
def get_crawler():
    return Crawler()


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


# test time do scrape a url
def test_url_scraping_time(get_scraper):
    start = time.time()
    _ = get_scraper.get_data_from_source("https://www.bbc.co.uk/")
    assert float(time.time() - start) < 2.0


# test time to scrape a pdf
# def test_pdf_scraping_time():
#     start = time.time()
#     # ERROR this link doesnt work with the current code
#     _ = pytest.scraper.get_data_from_source("www.africau.edu/images/default/sample.pdf")
#     assert float(time.time() - start) < 2.0

# TODO this currently fails, and gives looks like the google function might give non-deterministic results.
@pytest.mark.parametrize("keywords, n_results", [
    (["London", "England", "Big"], 25),
    (["Premier", "League", "Salah"], 20),
    (["Wet", "Weather", "Holiday"], 15),
    (["Test", "Google", "Random", "Elephant", "Nonsense"], 10)
])
# check google search returns correct # of results
def test_google_returns_x_results(keywords, n_results, get_crawler):
    urls_google = get_crawler.crawl_google_with_key_words(keywords, n_results)
    assert len(urls_google) == n_results


# check that scraped url has values in all of returned places
def test_url_scraping_values(get_scraper):
    scraped_data = get_scraper.get_data_from_source("https://www.bbc.co.uk/")
    assert scraped_data.uid == "" and scraped_data.content_type == "" and \
           all(v is not None for v in
               [scraped_data.url, scraped_data.raw_html, scraped_data.title, scraped_data.text_body, scraped_data.cleaned_tokens, scraped_data.html_links])


# need an example pdf document
# check that scraped pdf has values in all of returned places
# def test_pdf_scraping_values(data):
#     scraped_data = pytest.scraper.get_data_from_source("") # TODO
#     assert scraped_data.uid == "" and scraped_data.content_type == "" and \
#            all(v is not None for v in
#                [scraped_data.url, scraped_data.raw_html, scraped_data.title, scraped_data.text_body, scraped_data.cleaned_tokens, scraped_data.html_links])
#




# check twitter search returns correct # of results

# check correct number of key words are returned

#