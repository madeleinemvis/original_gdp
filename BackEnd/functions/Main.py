import random
from datetime import datetime

import cufflinks as cf
import pandas as pd
import plotly.express as px

from BackEnd.functions.analysis import NLPAnalyser
from BackEnd.functions.causal import Causal, TrendMap
from BackEnd.functions.dataretrieval import Crawler, Scraper
from BackEnd.functions.dbmanager import DbManager
from BackEnd.functions.textprocessing import TextProcessor

NUMBER_OF_KEY_WORDS = 30
NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
NUMBER_OF_TWEETS_RESULTS_WANTED = 20
MAXIMUM_URL_CRAWL_DEPTH = 3


def generate_manifesto(scraper, text_processor, source_urls, all_sentences, document_html_links, documents):
    urls = set()
    scraped_data = {}

    if len(all_sentences) == 0:
        url_dict = scraper.downloads(source_urls)
        for k in url_dict.keys():
            scraped_data[k] = url_dict[k]
            urls.update(url_dict[k].html_links)

        # if there are less than 5 documents, scrape tokens
        if len(source_urls) < 5:
            all_tokens = [t for s in scraped_data.values() for t in s.tokens]
            key_words_with_scores = TextProcessor.calculate_key_words(all_tokens, NUMBER_OF_KEY_WORDS)
        else:
            all_sentences = " ".join([s.text_body for s in scraped_data.values()])
            key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, NUMBER_OF_KEY_WORDS)

        print(f"Sources in manifesto: {len(source_urls)}")
        print(f"Sources found in manifesto sources: {len(urls)}")
    else:
        # If texts stored in database
        urls.update(document_html_links)
        key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, NUMBER_OF_KEY_WORDS)
        print(f"Sources in manifesto: {len(documents)}")
        print(f"Sources found in manifesto sources: {len(document_html_links)}")

    return urls, scraped_data, key_words_with_scores


def crawl_google(crawler, key_words):
    # TODO here we are using all 30 keywords for the google search,
    #  we might want to only use 5 or 6 to help with results
    urls_google = crawler.crawl_google(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    print(f"Top {NUMBER_OF_GOOGLE_RESULTS_WANTED} Google Results from Keywords ({key_words}):")
    for i, url in enumerate(urls_google):
        print(f"[{i + 1}]: {url}")
    return urls_google


def generate_suggested_urls(no_of_suggestions, google_urls, urls):
    # planning on asking for the approval on the google search results first and then if we want more suggestions,
    # we can add in random ones from the urls seem in the original documents
    if len(google_urls) < no_of_suggestions:
        suggestions = list(google_urls)
        return suggestions.extend(random.choices(list(urls), k=no_of_suggestions - len(google_urls)))
    else:
        return list(google_urls)[:no_of_suggestions]


def scrape_google_results(scraper, google_urls):
    data = scraper.downloads(google_urls)
    new_urls = set()
    new_scraped_data = {}
    if data is not None:
        for k in data.keys():
            new_scraped_data[k] = data[k]
            new_urls.update(data[k].html_links)
    return new_urls, new_scraped_data


# this is the function that makes the graphic,
def make_sentiment_scatter_plot(tweets):
    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    tweet_df = pd.DataFrame(tweets)
    fig = px.scatter(tweet_df, x='favorite_count', y='retweet_count', color='sentiment')
    return fig


def make_sentiment_pie_chart(tweets):
    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    tweet_df = pd.DataFrame(tweets)
    fig = px.pie(tweet_df, names='sentiment_score_cat')
    return fig


# Function for the main workflow of the project
def main(source_urls: [str], claim: str):
    start_t = datetime.now()
    analyser, crawler, scraper, text_processor, causal = NLPAnalyser(), Crawler(), Scraper(), TextProcessor(), Causal()
    db_manager = DbManager()

    print("-------- RETRIEVING DATA FROM DB MANAGER --------")
    uid = 'some_random_hash'
    documents = db_manager.get_all_documents(uid)
    all_sentences = db_manager.get_all_main_texts(uid)
    document_html_links = db_manager.get_all_html_links(uid)
    claim = db_manager.get_claim(uid)
    # TODO: implement - wantSuggestions = db_manager.get_want_suggestions('some_random_hash')
    want_suggestions = True
    # TODO: implement - no_of_suggestions = db_manager.get_no_of_suggestions('some_random_hash')
    no_of_suggestions = 25

    print("-------- MANIFESTO --------")
    urls, scraped_data, key_words_with_scores = generate_manifesto(scraper, text_processor, source_urls, all_sentences,
                                                                   document_html_links, documents)

    key_words = [k for k, v in key_words_with_scores]
    print(f"Top {NUMBER_OF_KEY_WORDS} keywords from manifesto: {key_words}")

    print("-------- CRAWLING GOOGLE --------")
    urls_google = crawl_google(crawler, key_words)

    if want_suggestions:
        print("---- GENERATING SUGGESTED URLS FOR USER ----")
        suggestions = generate_suggested_urls(no_of_suggestions, urls_google, urls)

    print("-------- SCRAPING GOOGLE URLS --------")
    # retrieve and store all the data about a URL
    new_urls, new_scraped_data = scrape_google_results(scraper, urls_google)
    urls.update(new_urls)
    scraped_data.update(new_scraped_data)

    print("-------- SCRAPING TWITTER --------")
    # crawling with Twitter
    crawled_tweets = crawler.twitter_crawl(uid, key_words, NUMBER_OF_TWEETS_RESULTS_WANTED)
    fig = make_sentiment_scatter_plot(crawled_tweets)
    fig.show()
    fig = make_sentiment_pie_chart(crawled_tweets)
    fig.show()

    # print("-------- EXAMPLE SIMILARITY CHECKING --------")
    # do some similarity checking for the documents so far crawled
    # Throws errors if links weren't searched 
    analyser.create_tfidf_model(scraped_data)

    print("-------- RECURSIVE CRAWLING --------")
    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    recursive_urls = crawler.url_cleaner(urls)
    final_crawled_urls = crawler.recursive_url_crawl(recursive_urls, MAXIMUM_URL_CRAWL_DEPTH, analyser)
    scraped_data.update(final_crawled_urls)
    print("------- SCRAPE REMAINING URLS -------")
    # retrieve and store all the data about a URL's not yet scraped
    urls_to_scrape = [u for u in urls if u not in scraped_data.keys()]
    data = scraper.downloads(urls_to_scrape)
    for k in data.keys():
        scraped_data[k] = data[k]

    print("-------- CAUSAL ANALYSIS --------")
    #causal_t = datetime.now()
    econ, health, politics = causal.analyse(key_words[:5])
    #print("Causal time: ", datetime.now()-causal_t)
    #trend = TrendMap()
    #trend_map = trend(key_words[:5])

    print("-------- STORING --------")
    # db_manager.insert_many('documents_document')  # Collection name for web pages

    db_manager.insert_many('tweets_tweet', crawled_tweets)  # Collection name for tweets
    # perform analysis on the scraped dataS

    # perform data visualisation

    # use api to communicate results to webpage
    print("Time taken for entire process: ", datetime.now()-start_t)


if __name__ == "__main__":
    sources = [
        "https://theirishsentinel.com/2020/08/10/depopulation-through-forced-vaccination-the-zero-carbon-solution/",
        "https://www.healthline.com/health/vaccinations/opposition",
        "https://ec.europa.eu/health/sites/health/files/vaccination/docs/2018_vaccine_confidence_en.pdf",
        "https://www.theguardian.com/world/2020/nov/10/coronavirus-anti-vaxxers-seek-to-discredit-pfizers-vaccine",
        "https://www.healthline.com/health/vaccinations/opposition"]
    main(sources, "vaccines cause autism")
