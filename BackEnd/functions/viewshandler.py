from ast import literal_eval

from django.utils.datastructures import MultiValueDictKeyError
from documents.models import Document, Claim
from tweets.models import Tweet, Query
from trends.models import Trend

from .article_sentiments import PredictSentiment
from .dataretrieval import Scraper
from .dbmanager import DbManager


# Handles all tasks that are used directly used by the end-point
# Setting/saving objects and reading request attachments
class ViewsHandler:
    db_manager = None
    scraper = Scraper()  # Extracts contents from files and URLs
    predict_sentiment = PredictSentiment()  # Extracts sentiment from Documents

    def __init__(self):
        self.db_manager = DbManager()  # Handles interactions with the Database

    # Scrapes a list of documents
    # Returns a list of Document objects from the Document model
    def read_docs(self, docs) -> [str]:
        documents = []
        try:
            docs = literal_eval(docs)  # Converts String into array of URLs
            for d in docs:
                documents.append(docs[d])
        except:
            documents.extend(docs)  # Appends list of files

        documents = self.scraper.downloads(documents)  # Scrapes list of documents, returns a dictionary
        doc_list = []
        for d in documents:  # For each document URL (d is the URL)
            doc_list.append(documents[d])  # For each documents, return the Data object (The Document)

        return doc_list

    # Returns Document object with Document model
    # Sets the UID, content_type, sentiment and stance prediction here as cannot be determined during scraping
    def set_documents(self, uid: str, content_type: str, documents, predictions_dict) -> [Document]:
        d_save = []
        for d in documents:
            # _id generated automatically
            try:
                prediction = predictions_dict[d.url]
                d_save.append(
                    Document(uid=uid, content_type=content_type, url=d.url, raw_html=d.raw_html, title=d.title,
                             text_body=d.text_body, cleaned_tokens=d.cleaned_tokens, html_links=d.html_links,
                             sentiment=self.predict_sentiment.get_article_sentiment_Afinn(d.text_body),
                             stance=prediction))
            except Exception as e:
                print("URL is not classified. Error: ", e)

        return d_save

    # Returns a list of Tweet objects with Tweet model
    @staticmethod
    def set_tweets(uid: str, tweets) -> [Tweet]:
        t_save = []
        for t in tweets:
            # _id generated automatically
            t_save.append(Tweet(uid=uid, screen_name=t['screen_name'], created_at=t['created_at'], text=t['text'],
                                favorite_count=t['favorite_count'],
                                retweet_count=t['retweet_count'], user_location=t['user_location'],
                                sentiment=t['sentiment']))
        return t_save

    # Returns Claim object with Claim model
    @staticmethod
    def set_claim(uid: str, claim: str) -> Claim:
        c_save = Claim(uid=uid, claim=claim)
        return c_save

    # Returns the Query object with Query model
    @staticmethod
    def set_query(uid: str, query: str) -> Query:
        q_save = Query(uid=uid, query=query)
        return q_save

    # Returns the Trend object with Trend model
    @staticmethod
    def set_trends(uid, e, h, p, mc, mt):
        t_save = [Trend(uid=uid, econ_count=e.value, econ_estimate=e.estimate, econ_random=e.random,
                        econ_unobserved=e.unobserved, econ_placebo=e.placebo, econ_subset=e.subset,
                        health_count=h.value, health_estimate=h.estimate, health_random=h.random,
                        health_unobserved=h.unobserved, health_placebo=h.placebo, health_subset=h.subset,
                        politics_count=p.value, politics_estimate=p.estimate, politics_random=p.random,
                        politics_unobserved=p.unobserved, politics_placebo=p.placebo, politics_subset=p.subset,
                        map_countries=mc, map_trends=mt)]
        return t_save

    # Takes a request and request form, extracts data
    # Returns the UID, claim, list of URLs, list of PDF URLs and list of Files
    @staticmethod
    def get_objects_from_request(request, request_form):
        uid = request_form.cleaned_data['uid']
        claim = request_form.cleaned_data['claim']
        document_urls = request_form.cleaned_data['urls']
        document_pdfs = request_form.cleaned_data['pdfs']
        files = None
        try:
            files = request.FILES.getlist('files')
        except MultiValueDictKeyError:
            pass
        return uid, claim, document_urls, document_pdfs, files

    # Stores all set Document objects into the database
    def save_documents(self, uid: str, content_type: str, documents, predictions_dict):
        d_save = self.set_documents(uid, content_type, documents, predictions_dict)
        Document.objects.bulk_create(d_save)

    # Stores the set Claim objects into the database
    def save_claim(self, uid: str, claim: str):
        c_save = self.set_claim(uid, claim)
        c_save.save()

    # Stores the set Query objects into the database
    def save_query(self, uid: str, query: str):
        q_save = self.set_query(uid, query)
        q_save.save()

    # Stores all set Tweets objects into the database
    def save_tweets(self, uid: str, tweets):
        t_save = self.set_tweets(uid, tweets)
        Tweet.objects.bulk_create(t_save)

    # Stores the set Trend objects into the database
    def save_trends(self, uid: str, econ, health, politics, map_countries, map_trends):
        t_save = self.set_trends(uid, econ, health, politics, map_countries, map_trends)
        Trend.objects.bulk_create(t_save)
