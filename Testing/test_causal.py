import pytest
import sys
sys.path.append('/Users/alexllewellyn/GDP/main-project')
from BackEnd.functions.causal import Causal


@pytest.fixture
def get_causal():
    return Causal()

def test_recursive_crawler(get_crawler):
    pass
    # url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    # response_dict = get_crawler.recursive_url_crawl([url], 3)
    # print(response_dict[url].title)
    # assert response_dict[url].title == "Web Scraper Test Sites" and len(response_dict) == 1

