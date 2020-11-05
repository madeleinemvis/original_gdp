from datetime import datetime

from functions.webretrieval import Crawler, Scraper
from functions.textprocessing import TextProcessor
from BackEnd.DbManager import DbManager
from collections import namedtuple


def get_all_data_from_url(url: str) -> namedtuple:
    URL_data = namedtuple('URL_data', 'raw_HTML text_title, text_body cleaned_tokens')

    # scrape the URL
    scraper = Scraper()
    initial_html = scraper.scrape_url(url)

    # extract the meta data and main body of text from the scraped HTML 
    processor = TextProcessor()
    title, main_text = processor.extract_main_body_from_html(initial_html)

    # make the tokens from the main text, and create a clean form
    tokens = processor.create_tokens_from_text(main_text)
    cleaned_tokens = processor.clean_tokens(tokens)

    return URL_data(raw_HTML=initial_html, text_title=title, text_body=main_text, cleaned_tokens=cleaned_tokens)


# Function for the main workflow of the project
def main():
    NUMBER_OF_KEY_WORDS = 5
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 100
    MAXIMUM_URL_CRAWL_DEPTH = 3

    processor = TextProcessor()
    crawler = Crawler()
    db_api = DbManager()

    start_t = datetime.now()
    documents_queried = db_api.find_documents("WebURLs", "body", "vaccin*")
    time_taken = datetime.now()-start_t
    queried_count = db_api.count_documents("WebURLs", "body", "vaccin*")

    print("Time to query: ", time_taken, " for ", queried_count, " documents.")

    # Using a dictionary of mapping URL to data for an initial data storage method, will likely need to change
    # very soon
    scraped_data = {}

    print("-------- MANIFESTO --------")
    print("*** SCRAPING ***")
    # start with the initial URL
    # TODO: Being able to take in multiple URLs
    start_url = "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/?fbclid=IwAR017eZePLsduO5ZaxM3X8dFkipeQqy58Go8eL3SkuQ4YFtRVSjfBwDMD0A"
    """ Other URLS:
    - https://vactruth.com/2018/08/30/vaccine-induced-autism/ # faulty (Forbidden with crawler) 
    - https://vactruth.com/2018/05/02/alfie-evans-timeline/
    - https://vactruth.com/2019/06/07/the-vaccination-that-never-should-have-been-approved/
    - https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/?fbclid=IwAR017eZePLsduO5ZaxM3X8dFkipeQqy58Go8eL3SkuQ4YFtRVSjfBwDMD0A
    """
    # TODO: Testing faulty urls for scraping

    scraped_data[start_url] = get_all_data_from_url(start_url)

    # find all URLs in initial document
    urls = processor.extract_urls_from_html(scraped_data[start_url].raw_HTML)

    print("*** KEYWORDS ***")
    # calculate key words from manifesto
    key_words = processor.calculate_key_words(scraped_data[start_url].cleaned_tokens,
                                              NUMBER_OF_KEY_WORDS)  # TODO: Testing of wild cards with Google searching

    print("-------- CRAWLING --------")
    # look to crawl with the new data
    crawled_urls = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    urls.extend(crawled_urls)

    # crawling with Twitter, returns JSON object
    crawled_tweets = crawler.twitter_crawl(key_words, NUMBER_OF_TWEETS_RESULTS_WANTED)
    # TODO: Sanitise and Store tweets (TwitterData collection)

    # do some similarity checking for the documents so far crawled

    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    final_crawled_urls = crawler.recursive_url_crawl(urls, MAXIMUM_URL_CRAWL_DEPTH)
    urls.extend(final_crawled_urls)

    print("-------- WEB SCRAPING --------")
    # retrieve and store all the data about a URL
    urls_list = []
    for url in urls:
        start_t = datetime.now()
        print("Scraping: " + url)
        scraped_data[url] = get_all_data_from_url(url)
        # Create dictionary for input
        url_insert = {"title": getattr(scraped_data[url], "text_title"),
                      "body": getattr(scraped_data[url], "text_body")
                      }
        urls_list.append(url_insert)
        print("Time Taken: ", (datetime.now()-start_t))

    print("-------- STORING --------")
    url_col = "WebURLs"
    db_api.insert_many(url_col, urls_list)

    # perform analysis on the scraped data

    # perform data visualisation

    # use api to communicate results to webpage


if __name__ == "__main__":
    main()
