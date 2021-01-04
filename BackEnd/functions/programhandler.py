import random
import json
from csv import DictWriter


import csv
from functions.dataretrieval import Scraper, Crawler
from functions.analysis import NLPAnalyser
from functions.textprocessing import TextProcessor
from functions.causal import Causal, TrendMap
from functions.StanceDetection.pred import PredictStance
from functions.article_sentiments import PredictSentiment


class Handler:
    NUMBER_OF_KEY_WORDS = 25
    NUMBER_OF_SUGGESTED = 15
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 20
    MAXIMUM_URL_CRAWL_DEPTH = 3

    def __init__(self):
        self.scraper = Scraper()
        self.crawler = Crawler()
        self.text_processor = TextProcessor()
        self.causal = Causal()
        self.trend_map = TrendMap()
        self.predict_stance = PredictStance()

    def generate_manifesto(self, documents):
        urls = set()
        scraped_data = {}
        for d in documents:
            scraped_data[d.url] = d
            urls.update(d.html_links)

        # if there are less than 5 documents, scrape tokens
        if len(documents) < 5:
            all_tokens = [t for d in documents for t in d.cleaned_tokens]
            keywords = TextProcessor.calculate_key_words(all_tokens, self.NUMBER_OF_KEY_WORDS)
        else:
            all_sentences = " ".join([d.text_body for d in documents])
            keywords = self.text_processor.calculate_keywords_with_text_rank(all_sentences,
                                                                             self.NUMBER_OF_KEY_WORDS)

        print(f"Sources in manifesto: {len(documents)}")
        print(f"Sources found in manifesto sources: {len(urls)}")
        return urls, scraped_data, keywords

    # Returns list of keywords and their corresponding value
    def get_all_keywords(self, documents):
        if len(documents) < 5:
            all_tokens = [t for d in documents for t in d.cleaned_tokens]
            return [t[0] for t in self.text_processor.calculate_key_words(all_tokens, self.NUMBER_OF_KEY_WORDS)]
        else:
            all_sentences = " ".join([d.text_body for d in documents])
            return [t[0] for t in
                    self.text_processor.calculate_keywords_with_text_rank(all_sentences, self.NUMBER_OF_KEY_WORDS)]

    # {documents} are only source documents.
    @staticmethod
    def get_all_html_links(documents):  # TODO: is documents Document from model?
        urls = set()
        # Get all HTML links
        for d in documents:
            urls.update(d.html_links)

        print(f"Sources in manifesto: {len(documents)}")
        print(f"Sources found in manifesto sources: {len(urls)}")
        return urls

    def crawl_google(self, keywords):
        urls_google = self.crawler.crawl_google(keywords, self.NUMBER_OF_GOOGLE_RESULTS_WANTED)
        print(f"Top {self.NUMBER_OF_GOOGLE_RESULTS_WANTED} Google Results from Keywords ({keywords[:5]}):")
        for i, url in enumerate(urls_google):
            print(f"[{i + 1}]: {url}")
        return urls_google

    def crawl_google_suggested(self, keywords):
        urls_google = self.crawler.crawl_google(keywords, self.NUMBER_OF_SUGGESTED)
        print(f"Top {self.NUMBER_OF_SUGGESTED} Google Results from Keywords ({keywords[:5]}):")
        for i, url in enumerate(urls_google):
            print(f"[{i + 1}]: {url}")
        return urls_google

    def generate_suggested_urls(self, documents):
        # planning on asking for the approval on the google search results first and then if we want more suggestions,
        # we can add in random ones from the urls seem in the original documents
        keywords = self.get_all_keywords(documents)
        urls = self.get_all_html_links(documents)
        google_urls = self.crawl_google_suggested(keywords)
        if len(google_urls) < self.NUMBER_OF_SUGGESTED:
            suggestions = list(google_urls)
            return suggestions.extend(random.choices(list(urls), k=self.NUMBER_OF_SUGGESTED - len(google_urls)))
        else:
            return list(google_urls)[:self.NUMBER_OF_SUGGESTED]

    def scrape_google_results(self, google_urls):
        data = self.scraper.downloads(google_urls)
        new_urls = set()
        new_scraped_data = {}
        if data is not None:
            for k in data.keys():
                new_scraped_data[k] = data[k]
                new_urls.update(data[k].html_links)
        return new_urls, new_scraped_data

    def trends_analysis(self, keywords):
        econ, health, politics = self.causal.analyse(keywords[:5])
        map_data = self.trend_map.map_maker(keywords[:5])
        map_countries = json.dumps(map_data.countries)
        map_trends = json.dumps(map_data.trends)
        return econ, health, politics, map_countries, map_trends

    def run_program(self, viewshandler, uid: str, claim: str, documents):
        print("------- CLEARING OUT THE DATABASE --------)")
        # viewshandler.db_manager.drop_collection('documents_document')
        # viewshandler.db_manager.drop_collection('documents_claim')
        # viewshandler.db_manager.drop_collection('tweets_tweet')
        # viewshandler.db_manager.drop_collection('trends_trend')
        nlpanalyser = NLPAnalyser()

        print("-------- MANIFESTO --------")
        urls, scraped_data, key_words_with_scores = self.generate_manifesto(documents)

        keywords = [k for k, v in key_words_with_scores]
        print(f"Top {self.NUMBER_OF_KEY_WORDS} keywords from manifesto: {keywords}")

        print("-------- CRAWLING GOOGLE --------")
        urls_google = self.crawl_google(keywords)
        
        print("-------- SCRAPING GOOGLE URLS --------")
        # retrieve and store all the data about a URL
        new_urls, new_scraped_data = self.scrape_google_results(urls_google)
        urls.update(new_urls)
        scraped_data.update(new_scraped_data)

        print("-------- CREATE TF-IDF MODEL --------")
        nlpanalyser.create_tfidf_model(scraped_data)

        print("-------- SCRAPING TWITTER --------")
        # crawling with Twitter
        crawled_tweets = self.crawler.twitter_crawl(uid, keywords, self.NUMBER_OF_TWEETS_RESULTS_WANTED)

        print("-------- CAUSAL ANALYSIS --------")
        # econ, heath, politics, map_countries, map_trends = self.trends_analysis(keywords[:5])

        # print("-------- RECURSIVE CRAWLING --------")
        # # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
        # recursive_urls = self.crawler.url_cleaner(urls)
        # final_crawled_urls = self.crawler.recursive_url_crawl(recursive_urls, self.MAXIMUM_URL_CRAWL_DEPTH, nlpanalyser)
        # scraped_data.update(final_crawled_urls)
        # print("------- SCRAPE REMAINING URLS -------")
        # # retrieve and store all the data about a URL's not yet scraped
        # urls_to_scrape = [u for u in urls if u not in scraped_data.keys()]
        # data = self.scraper.downloads(urls_to_scrape)
        # for k in data.keys():
        #     scraped_data[k] = data[k]

        print("-------- TEST DATA PREPARATION --------")

        name = "functions/StanceDetection/test_stances_" + uid
        stances = "%s.csv" % name

        with open(stances, 'w') as csvfile:
            fieldnames = ['Headline', 'Body ID']
            writer = DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for index, item in enumerate(list(scraped_data.keys())):
                writer.writerow({'Headline': claim, 'Body ID': index})

        name = "functions/StanceDetection/test_bodies_" + uid
        bodies = "%s.csv" % name

        with open(bodies, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Body ID', 'articleBody']
            writer = DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for index, item in enumerate(list(scraped_data.values())):
                writer.writerow({'Body ID': index, 'articleBody': item.text_body})

        print("-------- STANCE DETECTION --------")

        predictions_dict = self.predict_stance.getPredictions(stances, bodies, list(scraped_data.keys()))
        print("predictions dict:", predictions_dict)

        print("-------- STORING TWEETS --------")
        viewshandler.save_tweets(uid, crawled_tweets)

        # print("-------- STORING TRENDS --------")
        # viewshandler.save_trends(uid, econ, heath, politics, map_countries, map_trends)

        print("------- STORE NEW DOCUMENTS -------")
        viewshandler.save_documents(uid, 'web-page', scraped_data.values(), predictions_dict)
