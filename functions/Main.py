from functions.dataretrieval import Crawler, Scraper
from functions.textprocessing import TextProcessor
from functions.analysis import NLP_Analyser


# Function for the main workflow of the project
def main(source_urls: [str]):
    NUMBER_OF_KEY_WORDS = 5
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 100
    MAXIMUM_URL_CRAWL_DEPTH = 3

    processor = TextProcessor()
    crawler = Crawler()
    analyser = NLP_Analyser()

    alt_url = "https://www.bbc.co.uk/news/uk-54779430"
    source_urls.append(alt_url)

    # Using a dictionary of mapping URL to data for an initial data storage method, will likely need to change
    # very soon
    scraped_data = {}

    print("-------- MANIFESTO --------")

    # go through each source input and store the main body text, and cleaned tokens
    # along with the html links found
    urls = set()

    # TODO we have a problem with key words,
    # do we want the top 'x' keywords across the documents or do we want the top 'x' from each of the documents
    for source in source_urls:
        data = Scraper.get_data_from_source(source)
        scraped_data[source] = Scraper.get_data_from_source(source)
        urls.update(data.html_links)

    all_tokens = [t for s in scraped_data.values() for t in s.tokens]
    key_words = TextProcessor.calculate_key_words(all_tokens, NUMBER_OF_KEY_WORDS)

    print(f"Sources in manifesto: {len(sources)}")
    print(f"Sources found in manifesto sources: {len(urls)}")
    print(f"Top {NUMBER_OF_KEY_WORDS} keywords form manifesto: {key_words}")

    print("-------- CRAWLING --------")
    # look to crawl with the new data
    urls_google = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)

    print("-------- SCRAPING & STORING --------")
    # retrieve and store all the data about a URL
    for url in urls_google:
        scraped_data[url] = Scraper.get_data_from_source(url)
        # TODO: Store URL data

    analyser.create_topic_model(scraped_data)
    print("Similar Doc:", analyser.check_similarity(scraped_data[source_urls[0]]))
    print("Non-similar doc:", analyser.check_similarity(scraped_data[alt_url]))

    # crawling with Twitter, returns JSON object
    crawled_tweets = crawler.twitter_crawl(key_words, NUMBER_OF_TWEETS_RESULTS_WANTED)
    for tweet in crawled_tweets:
        print(tweet)
    # do some similarity checking for the documents so far crawled

    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    final_crawled_urls = crawler.recursive_url_crawl(urls, MAXIMUM_URL_CRAWL_DEPTH)
    urls.update(final_crawled_urls)

    print("-------- SCRAPING & STORING --------")
    # retrieve and store all the data about a URL's not yet scraped
    urls_to_scrape = [u for u in urls if u not in scraped_data.keys()]
    for url in urls_to_scrape:
        scraped_data[url] = Scraper.get_data_from_source(url)

    # perform analysis on the scraped data

    # perform data visualisation

    # use api to communicate results to webpage


if __name__ == "__main__":
    # start with the initial URL
    start_url = "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/"
    """ Other URLS:
    - https://vactruth.com/2018/08/30/vaccine-induced-autism/ # faulty (Forbidden with crawler)
    - https://vactruth.com/2018/05/02/alfie-evans-timeline/
    - https://vactruth.com/2019/06/07/the-vaccination-that-never-should-have-been-approved/
    - https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/
    """
    sources = [start_url]
    main(sources)
