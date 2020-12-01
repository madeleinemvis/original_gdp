from BackEnd.functions.dataretrieval import Crawler, Scraper
from BackEnd.functions.textprocessing import TextProcessor
from BackEnd.dbmanager import DbManager


# Function for the main workflow of the project
def main(source_urls: [str], claim: str):
    NUMBER_OF_KEY_WORDS = 30
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 20
    MAXIMUM_URL_CRAWL_DEPTH = 3

    crawler = Crawler()
    db_manager = DbManager()
    scraper = Scraper()
    text_processor = TextProcessor()
    
    # Using a dictionary of mapping URL to data for an initial data storage method, will likely need to change
    # very soon
    scraped_data = {}

    print("-------- MANIFESTO --------")

    # go through each source input and store the main body text, and cleaned tokens
    # along with the html links found
    urls = set()

    documents = db_manager.get_all_documents('some_random_hash')
    all_sentences = db_manager.get_all_main_texts('some_random_hash')
    document_html_links = db_manager.get_all_html_links('some_random_hash')
    claim = db_manager.get_claim('some_random_hash')

    # if no tokens stored in database
    if len(all_sentences) == 0:
        for source in source_urls:
            data = scraper.scrape_url(source)
            scraped_data[source] = data
            urls.update(data.html_links)

        # if there are less than 5 documents, scrape tokens
        if len(source_urls) < 5:
            all_tokens = [t for s in scraped_data.values() for t in s.tokens]
            key_words_with_scores = TextProcessor.calculate_key_words(all_tokens, NUMBER_OF_KEY_WORDS)
            key_words = [k for k, v in key_words_with_scores]
            print(f"Most frequent key_words: {key_words}")
        else:
            all_sentences = " ".join([s.text_body for s in scraped_data.values()])
            key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, NUMBER_OF_KEY_WORDS)
            key_words = [word for word, score in key_words_with_scores]

        print(f"Sources in manifesto: {len(source_urls)}")
        print(f"Sources found in manifesto sources: {len(urls)}")
    else:
        # If texts stored in database
        key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, NUMBER_OF_KEY_WORDS)
        key_words = [word for word, score in key_words_with_scores]
        urls.update(document_html_links)
        print(f"Sources in manifesto: {len(documents)}")
        print(f"Sources found in manifesto sources: {len(document_html_links)}")

    print(f"Top {NUMBER_OF_KEY_WORDS} keywords form manifesto: {key_words}")

    print("-------- CRAWLING GOOGLE --------")
    # look to crawl with the new data
    urls_google = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    print(f"Top {NUMBER_OF_GOOGLE_RESULTS_WANTED} Google Results from Keyword {key_words}:")
    for i, url in enumerate(urls_google):
        print(f"[{i + 1}]: {url}")

    print("-------- SCRAPING GOOGLE URLS --------")
    # retrieve and store all the data about a URL
    data = scraper.downloads(urls_google)
    if data is not None:
        for k in data.keys():
            scraped_data[k] = data[k]
            urls.update(data[k].html_links)

    print("-------- SCRAPING TWITTER --------")
    # crawling with Twitter
    crawled_tweets = crawler.twitter_crawl(key_words, NUMBER_OF_TWEETS_RESULTS_WANTED)

    # print("-------- EXAMPLE SIMILARITY CHECKING --------")
    # do some similarity checking for the documents so far crawled
    # Throws errors if links weren't searched 
    #analyser.create_topic_model(scraped_data)
    #print("Similar Doc:", analyser.check_similarity(scraped_data["https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/"]))
    #print("Non-similar doc:", analyser.check_similarity(scraped_data["https://www.bbc.co.uk/news/uk-54779430"]))

    print("-------- RECURSIVE CRAWLING --------")
    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    recursive_urls = crawler.url_cleaner(urls)
    final_crawled_urls = crawler.recursive_url_crawl(recursive_urls, MAXIMUM_URL_CRAWL_DEPTH)
    scraped_data.update(final_crawled_urls)
    print("------- SCRAPE REMAINING URLS -------")
    # retrieve and store all the data about a URL's not yet scraped
    urls_to_scrape = [u for u in urls if u not in scraped_data.keys()]
    data = scraper.downloads(urls_to_scrape)
    for k in data.keys():
        scraped_data[k] = data[k]

    print("-------- STORING --------")
    db_manager.insert_many('documents_document')  # Collection name for web pages

    db_manager.insert_many('tweets_tweet', crawled_tweets)  # Collection name for tweets
    # perform analysis on the scraped dataS

    # perform data visualisation

    # use api to communicate results to webpage


if __name__ == "__main__":
    # start with the initial URL
    sources = [
        "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/",
        "https://www.healthline.com/health/vaccinations/opposition",
        "https://ec.europa.eu/health/sites/health/files/vaccination/docs/2018_vaccine_confidence_en.pdf",
        "https://www.theguardian.com/world/2020/nov/10/coronavirus-anti-vaxxers-seek-to-discredit-pfizers-vaccine",
        "https://www.healthline.com/health/vaccinations/opposition"]
    main(sources, "vaccines cause autism")
