from random import random

from BackEnd.documents.models import Document
from BackEnd.functions.dataretrieval import Scraper
from BackEnd.functions.textprocessing import TextProcessor


class Handler:
    NUMBER_OF_KEY_WORDS = 30
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    NUMBER_OF_TWEETS_RESULTS_WANTED = 20
    MAXIMUM_URL_CRAWL_DEPTH = 3
    scraper = None
    text_processor = None

    def __init__(self):
        scraper = Scraper()
        text_processor = TextProcessor()

    # def generate_manifesto(scraper, text_processor, source_urls, all_sentences, document_html_links, documents):
    #     urls = set()
    #     scraped_data = {}
    #
    #     if len(all_sentences) == 0:
    #         for source in source_urls:
    #             data = scraper.scrape_url(source)
    #             scraped_data[source] = data
    #             urls.update(data.html_links)
    #
    #         # if there are less than 5 documents, scrape tokens
    #         if len(source_urls) < 5:
    #             all_tokens = [t for s in scraped_data.values() for t in s.tokens]
    #             key_words_with_scores = TextProcessor.calculate_key_words(all_tokens, NUMBER_OF_KEY_WORDS)
    #         else:
    #             all_sentences = " ".join([s.text_body for s in scraped_data.values()])
    #             key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, NUMBER_OF_KEY_WORDS)
    #
    #         print(f"Sources in manifesto: {len(source_urls)}")
    #         print(f"Sources found in manifesto sources: {len(urls)}")
    #     else:
    #         # If texts stored in database
    #         urls.update(document_html_links)
    #         key_words_with_scores = text_processor.calculate_keywords_with_text_rank(all_sentences, self.NUMBER_OF_KEY_WORDS)
    #         print(f"Sources in manifesto: {len(documents)}")
    #         print(f"Sources found in manifesto sources: {len(document_html_links)}")
    #
    #     return urls, scraped_data, key_words_with_scores

    # TODO: is documents Document from model?
    def get_keywords(self, documents):
        # if there are less than 5 documents, scrape tokens
        if len(documents) < 5:
            all_tokens = [t for d in documents for t in d.cleaned_tokens]
            key_words_with_scores = self.text_processor.calculate_key_words(all_tokens, self.NUMBER_OF_KEY_WORDS)
        else:
            all_sentences = " ".join([d.text_body for d in documents])
            key_words_with_scores = self.text_processor.calculate_keywords_with_text_rank(all_sentences,
                                                                                          self.NUMBER_OF_KEY_WORDS)

            print(f"Sources in manifesto: {len(documents)}")
            print(f"Sources found in manifesto sources: {len(urls)}")

    def crawl_google(crawler, key_words):
        # TODO here we are using all 30 keywords for the google search,
        #  we might want to only use 5 or 6 to help with results
        urls_google = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
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
