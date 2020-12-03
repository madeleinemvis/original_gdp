import random

from functions.dataretrieval import Scraper, Crawler
from functions.textprocessing import TextProcessor


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

    def generate_manifesto(self, documents):
        urls = self.get_all_html_links(documents)
        keywords = self.get_all_keywords(documents)
        return urls, keywords

    # Returns list of keywords and their corresponding value
    def get_all_keywords(self, documents):
        if len(documents) < 5:
            all_tokens = [t for d in documents for t in d.cleaned_tokens]
            return [t[0] for t in self.text_processor.calculate_key_words(all_tokens, self.NUMBER_OF_KEY_WORDS)]
        else:
            all_sentences = " ".join([d.text_body for d in documents])
            return [t[0] for t in self.text_processor.calculate_keywords_with_text_rank(all_sentences, self.NUMBER_OF_KEY_WORDS)]

    # {documents} are only source documents.
    @staticmethod
    def get_all_html_links(documents): # TODO: is documents Document from model?
        urls = set()
        # Get all HTML links
        for d in documents:
            urls.update(d.html_links)

        print(f"Sources in manifesto: {len(documents)}")
        print(f"Sources found in manifesto sources: {len(urls)}")
        return urls

    def crawl_google(self, keywords, number_of_results):
        urls_google = self.crawler.crawl_google_with_key_words(keywords, number_of_results)
        print(f"Top {number_of_results} Google Results from Keywords ({keywords}):")
        for i, url in enumerate(urls_google):
            print(f"[{i + 1}]: {url}")
        return urls_google

    def crawl_google_suggested(self, keywords):
        urls_google = self.crawler.crawl_google_with_key_words(keywords, self.NUMBER_OF_SUGGESTED)
        print(f"Top {self.NUMBER_OF_SUGGESTED} Google Results from Keywords ({keywords}):")
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
