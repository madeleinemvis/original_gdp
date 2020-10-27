from webretrieval import Crawler, Scraper
from textprocessing import TextProcessor
from collections import namedtuple

def get_all_data_from_url(url: str) -> namedtuple:
    URL_data = namedtuple('URL_data', 'raw_HTML meta_data text_body cleaned_tokens')
    
    # scrape the URL
    scraper = Scraper()
    initial_html = scraper.scape_url(url)

    # extract the meta data and main body of text from the scraped HTML 
    processor = TextProcessor()
    meta_data = processor.extract_meta_data_from_HTML(initial_html)
    main_text = processor.extract_main_body_from_HTML(initial_html)

    # make the tokens from the main text, and create a clean form
    tokens = processor.create_tokens_from_text(main_text)
    cleaned_tokens = processor.clean_tokens(tokens)

    return URL_data(raw_HTML=initial_html, meta_data=meta_data, text_body=main_text, cleaned_tokens=cleaned_tokens)

# Function for the main workflow of the project
def main():
    NUMBER_OF_KEY_WORDS = 5
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    MAXIMUM_URL_CRAWL_DEPTH = 3

    # Using a dictionary of mapping URL to data for an initial data storage method, will likely need to change
    # very soon
    
    scraped_data = {}
        
    # start with the intitial URL
    start_URL = ""
    scraped_data[start_URL] = get_all_data_from_url(start_URL)  

    processor = TextProcessor()  
    
    # find all URLs in initial document
    urls = processor.extract_urls_from_HTML(scraped_data[start_URL].raw_HTML)
    
    # calculate key words from manefesto
    key_words = processor.calculate_key_words(scraped_data[start_URL].cleaned_tokens, NUMBER_OF_KEY_WORDS) 

    # look to crawl with the now know data
    crawler = Crawler()
    crawled_urls = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    
    urls.extend(crawled_urls)

    # do some similarity checking for the documents so far crawled


    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    final_crawled_urls = crawler.recursive_url_crawl(urls, MAXIMUM_URL_CRAWL_DEPTH)
    urls.extend(final_crawled_urls)
    
    # retrieve and store all the data about a URL
    for url in urls:
        scraped_data[url] = get_all_data_from_url(url)

    # perform analysis on the scraped data 

    # perform data visualisation

    # use api to communicate results to webpage

    



    



if __name__ == "__main__":
    main()