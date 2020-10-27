from webretrieval import Crawler, Scraper
from textprocessing import TextProcessor
from collections import namedtuple

# Function for the main workflow of the project
def main():
    NUMBER_OF_KEY_WORDS = 5
    NUMBER_OF_GOOGLE_RESULTS_WANTED = 25
    MAXIMUM_URL_CRAWL_DEPTH = 3

    # start with the intitial URL
    start_URL = ""


    # scrape the URL
    scraper = Scraper()
    initial_html = scraper.scape_url(start_URL)

    # extract the meta data and main body of text from the scraped HTML 
    processor = TextProcessor()
    meta_data = processor.extract_meta_data_from_HTML(initial_html)
    main_text = processor.extract_main_body_from_HTML(initial_html)
    urls = processor.extract_urls_from_HTML(initial_html)

    # make the tokens from the main text, and create a clean form
    tokens = processor.create_tokens_from_text(main_text)
    cleaned_tokens = processor.clean_tokens(tokens)

    key_words = processor.calculate_key_words(cleaned_tokens, NUMBER_OF_KEY_WORDS) 

    # look to crawl with the now know data
    crawler = Crawler()
    crawled_urls = crawler.crawl_google_with_key_words(key_words, NUMBER_OF_GOOGLE_RESULTS_WANTED)
    
    urls.extend(crawled_urls)

    # do some similarity checking for the documents so far crawled

    # recursively crawl the links upto certain depth - includes batch checking so these are the final documents
    final_crawled_urls = crawler.recursive_url_crawl(urls, MAXIMUM_URL_CRAWL_DEPTH)
    urls.extend(final_crawled_urls)

    # building a dictionary of url to data for that document
    # we now need a data storage method of some sort as there could potentially be a large volume of data here
    scraped_data = {}
    URL_data = namedtuple('URL_data', 'raw_HTML meta_data text_body cleaned_tokens')
    # this for loop would likely need to be its own method and could be very different, this is just an intial idea
    for url in urls:
        html = scraper.scape_url(url)
        meta_data = processor.extract_meta_data_from_HTML(html)
        text = processor.extract_main_body_from_HTML(html)
        tokens = processor.create_tokens_from_text(text)
        clean_tokens = processor.clean_tokens(tokens)
        scraped_data[url] = URL_data(raw_HTML=html, meta_data=meta_data, text_body=text, cleaned_tokens=clean_tokens)

    # perform analysis on the scraped data 

    # perform data visualisation

    # use api to communicate results to webpage

    



    



if __name__ == "__main__":
    main()