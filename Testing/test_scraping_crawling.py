import pytest
from BackEnd.functions.dataretrieval import Scraper, Crawler
import time
import requests
import os


@pytest.fixture
def get_scraper():
    return Scraper()


@pytest.fixture
def get_crawler():
    return Crawler()


# TODO Alex Lockwood, are there any edge cases that need to be added here?
@pytest.mark.parametrize("test_url", [
    "https://www.bbc.co.uk/",
    "https://www.theguardian.com/uk",
    "https://en.wikipedia.org/wiki/Pope_John_Paul_II",
    "https://www.xbox.com/en-GB/consoles/xbox-series-x",
    "https://www.bbc.co.uk/sport/football/championship/table",
    "https://www.whitehouse.gov/about-the-white-house/the-executive-branch/"
])
# check that scraped url has values in all of returned places
# TODO Alex Lockwood, all tests are getting ERROR "UnicodeEncodeError: 'charmap'
#  codec can't encode character '\u0142' in position 11335: character maps to <undefined>"
def test_url_scraping_values(get_scraper, test_url):
    response = requests.get(test_url)
    scraped_data = get_scraper.get_data_from_source(test_url, response)
    assert scraped_data.uid == "" and scraped_data.content_type == "" and \
           all(v is not None for v in
               [scraped_data.url, scraped_data.raw_html, scraped_data.title, scraped_data.text_body, scraped_data.cleaned_tokens, scraped_data.html_links])


@pytest.mark.parametrize("pdf_url", [
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "http://www.pdf995.com/samples/pdf.pdf",
    "http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf",
    "https://www.pubmedcentral.nih.gov/picrender.fcgi?artid=2480896&blobtype=pdf",
    "https://www.antennahouse.com/hubfs/xsl-fo-sample/pdf/basic-link-1.pdf?hsLang=en",
    "https://www.dpconline.org/docs/miscellaneous/events/163-document-formats-and-image-formats-king/file"
])
# check that scraped pdf has values in all of returned places
# Content type fails for: https://www.pubmedcentral.nih.gov/picrender.fcgi?artid=2480896&blobtype=pdf
# TODO Alex Lockwood ^
def test_pdf_scraping_values(get_scraper, pdf_url):
    request = requests.get(pdf_url)
    scraped_data = get_scraper.get_data_from_source(
        pdf_url, request)
    assert scraped_data.uid == "" and scraped_data.content_type == "application/pdf" and \
           all(v is not None for v in
               [scraped_data.url, scraped_data.raw_html, scraped_data.title, scraped_data.text_body, scraped_data.cleaned_tokens, scraped_data.html_links])


# used in more than one test so is a fixture
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
# TODO Maddy this currently fails
def test_google_returns_n_results(search_keywords_n_results, get_crawler):
    for keywords, n_results in search_keywords_n_results:
        assert len(get_crawler.crawl_google_with_key_words(keywords, n_results)) == n_results


# check twitter search returns correct # of results
# TODO Maddy this currently fails
def test_twitter_returns_n_results(search_keywords_n_results, get_crawler):
    for keywords, n_results in search_keywords_n_results:
        assert len(get_crawler.twitter_crawl("some-random-uid", keywords, n_results)) == n_results

# TODO Alex Lockwood, getting Error: "UnicodeEncodeError: 'charmap' codec can't encode character '\u0142'
#  in position 11335: character maps to <undefined>" for all calls so tests can run
def test_correct_data_returned_from_sources():
    test_genre = "Vaccine"
    for_path = os.path.join("Testing_Data", test_genre, "For")
    for filename in os.listdir(for_path):
        source_text = open(os.path.join(for_path, filename), "r", encoding="utf-8")
        lines = source_text.readlines()
        scraper = Scraper()
        url = lines[0]
        response = requests.get(url)
        data = scraper.get_data_from_source(url, response)

        assert data.title == lines[1] and data.text_body == lines[2]


# ##### ARCHIVED TESTS BELOW #########

# test time do scrape loads of urls is less than a benchmark TODO
# def test_url_scraping_time(get_scraper):
#     start = time.time()
#     _ = get_scraper.get_data_from_source("https://www.bbc.co.uk/")
#     assert float(time.time() - start) < 2.0

# test time to scrape a pdf
# def test_pdf_scraping_time():
#     start = time.time()
#     # ERROR this link doesnt work with the current code
#     _ = pytest.scraper.get_data_from_source("www.africau.edu/images/default/sample.pdf")
#     assert float(time.time() - start) < 2.0