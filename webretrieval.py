from bs4 import BeautifulSoup
import requests

# class for crawling and scraping the internet
class Crawler:
    def __init__(self):
        pass

    # Maddy
    # not sure how we want to use this method yet
    def crawl_google_with_key_words(self, key_words: [str], urls_returned: int) -> [str]:
        return []

    # recursively crawl a set of URLs with batch checking similarities
    def recursive_url_crawl(self, urls: [str], max_depth: int) -> [str]:
        return []
    


class Scraper:
    def __init__(self):
        pass
    
    # Alex Ll
    # method that returns all the HTML data from a URL
    def scape_url(self, URL: str) -> str:
        request = requests.get(URL)
        return request.text
