from functions.webretrieval import Crawler, Scraper
from functions.textprocessing import TextProcessor
from functions.analysis import NLP_Analyser
from collections import namedtuple


def get_all_data_from_url(url: str) -> namedtuple:
    URL_data = namedtuple('URL_data', 'raw_HTML meta_data text_body cleaned_tokens')

    # PDFs skipped, should be properly scraped through a PDF scraper
    if(url.endswith('.pdf')):
        return

    # scrape the URL
    scraper = Scraper()
    initial_html = scraper.scrape_url(url)

    # extract the meta data and main body of text from the scraped HTML 
    processor = TextProcessor()
    meta_data = processor.extract_meta_data_from_HTML(initial_html)  # to be ignored
    main_text = processor.extract_main_body_from_html(initial_html)

    # make the tokens from the main text, and create a clean form
    tokens = processor.create_tokens_from_text(main_text)
    cleaned_tokens = processor.clean_tokens(tokens)

    return URL_data(raw_HTML=initial_html, meta_data=meta_data, text_body=main_text, cleaned_tokens=cleaned_tokens)


# Function for the main workflow of the project
def main():
    NUMBER_OF_KEY_WORDS = 5
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 100
    MAXIMUM_URL_CRAWL_DEPTH = 3

    processor = TextProcessor()
    crawler = Crawler()
    analyser = NLP_Analyser()

    # Using a dictionary of mapping URL to data for an initial data storage method, will likely need to change
    # very soon
    scraped_data = {}

    print("-------- MANIFESTO --------")
    # start with the initial URL
    start_url = "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/?fbclid=IwAR017eZePLsduO5ZaxM3X8dFkipeQqy58Go8eL3SkuQ4YFtRVSjfBwDMD0A"
    start_url = "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/"
    """ Other URLS:
    - https://vactruth.com/2018/08/30/vaccine-induced-autism/ # faulty (Forbidden with crawler)
    - https://vactruth.com/2018/05/02/alfie-evans-timeline/
    - https://vactruth.com/2019/06/07/the-vaccination-that-never-should-have-been-approved/
    - https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/
    """

    scraped_data[start_url] = get_all_data_from_url(start_url)

    alt_url = "https://www.bbc.co.uk/news/uk-54779430"
    scraped_data[alt_url] = get_all_data_from_url(alt_url)

    # find all URLs in initial document
    urls = processor.extract_urls_from_html(scraped_data[start_url].raw_HTML)

    # calculate key words from manifesto
    key_words = processor.calculate_key_words(scraped_data[start_url].cleaned_tokens, NUMBER_OF_KEY_WORDS)

    print("-------- CRAWLING --------")
    urls_google = []
    # look to crawl with the new data
    crawled_urls = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    urls_google.extend(crawled_urls)

    print("-------- SCRAPING & STORING --------")
    # retrieve and store all the data about a URL
    for url in urls_google:
        scraped_data[url] = get_all_data_from_url(url)
        # TODO: Store URL data

    analyser.create_topic_model(scraped_data)
    print("Similar Doc:", analyser.check_similarity(scraped_data[start_url]))
    print("Non-similar doc:", analyser.check_similarity(scraped_data[alt_url]))

    # crawling with Twitter, returns JSON object
    crawled_tweets = crawler.twitter_crawl(key_words, NUMBER_OF_TWEETS_RESULTS_WANTED)
    for tweet in crawled_tweets:
        print(tweet)
    # do some similarity checking for the documents so far crawled

    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    final_crawled_urls = crawler.recursive_url_crawl(urls, MAXIMUM_URL_CRAWL_DEPTH)
    urls.extend(final_crawled_urls)

    print("-------- SCRAPING & STORING --------")
    # retrieve and store all the data about a URL
    for url in urls:
        scraped_data[url] = get_all_data_from_url(url)

    # perform analysis on the scraped data

    # perform data visualisation

    # use api to communicate results to webpage


if __name__ == "__main__":
    main()
