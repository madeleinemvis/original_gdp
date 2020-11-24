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


# test time do scrape loads of urls is less than a benchmark TODO
def test_url_scraping_time(get_scraper):
    start = time.time()
    _ = get_scraper.get_data_from_source("https://www.bbc.co.uk/")
    assert float(time.time() - start) < 2.0

# TODO check that blacklisting works for recursive crawling


# test time to scrape a pdf
# def test_pdf_scraping_time():
#     start = time.time()
#     # ERROR this link doesnt work with the current code
#     _ = pytest.scraper.get_data_from_source("www.africau.edu/images/default/sample.pdf")
#     assert float(time.time() - start) < 2.0


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


@pytest.fixture
def search_keywords_n_results():
    return [
        (["London", "England", "Big"], 25),
        (["Premier", "League", "Salah"], 20),
        (["Wet", "Weather", "Holiday"], 15),
        (["Test", "Search", "Random", "Elephant", "Nonsense"], 50),
        (["Test", "To", "Return", "Nothing"], 0),
        (["Test", "Return", "Negative"], -1),
        (["Test", "Too", "Many"], 10_000) # this would look for a time out or an error thrown
    ]


# check google search returns correct # of results
# TODO this currently fails
def test_google_returns_n_results(search_keywords_n_results, get_crawler):
    for keywords, n_results in search_keywords_n_results:
        assert len(get_crawler.crawl_google_with_key_words(keywords, n_results)) == n_results


# check twitter search returns correct # of results
# TODO this currently fails
def test_twitter_returns_n_results(search_keywords_n_results, get_crawler):
    for keywords, n_results in search_keywords_n_results:
        assert len(get_crawler.twitter_crawl(keywords, n_results)) == n_results
