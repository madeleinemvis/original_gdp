from ast import literal_eval

from django.utils.datastructures import MultiValueDictKeyError
from documents.models import Document, Claim
from tweets.models import Tweet

from .dataretrieval import Scraper
from .dbmanager import DbManager


class ViewsHandler:
    db_manager = None
    scraper = Scraper()

    def __init__(self):
        self.db_manager = DbManager()

    def read_docs(self, docs: str):
        docs = literal_eval(docs)
        
        documents = []
        for d in docs:
            documents.append(docs[d])
        documents = self.scraper.downloads(documents)
        
        doc_list = []
        for d in documents:
            doc_list.append(documents[d])
        
        return doc_list

    @staticmethod
    def set_documents(uid: str, content_type: str, documents):
        d_save = []
        for d in documents:
            # _id generated automatically
            d_save.append(Document(uid=uid, content_type=content_type, url=d.url, raw_html=d.raw_html, title=d.title,
                                   text_body=d.text_body, cleaned_tokens=d.cleaned_tokens, html_links=d.html_links))
        return d_save

    @staticmethod
    def set_tweets(uid: str, tweets):
        t_save = []
        for t in tweets:
            # _id generated automatically
            t_save.append(Tweet(uid=uid, created_at=t['created_at'], text=t['text'], favorite_count=t['favorite_count'],
                                retweet_count=t['retweet_count'], user_location=t['user_location'],
                                sentiment=t['sentiment']))
        return t_save

    @staticmethod
    def set_claim(uid, claim):
        c_save = Claim(uid=uid, claim=claim)
        return c_save

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

    def save_documents(self, uid: str, content_type: str, documents):
        d_save = self.set_documents(uid, content_type, documents)
        Document.objects.bulk_create(d_save)

    def save_claim(self, uid: str, claim: str):
        c_save = self.set_claim(uid, claim)
        c_save.save()

    def save_tweets(self, uid: str, tweets):
        t_save = self. set_tweets(uid, tweets)
        Tweet.objects.bulk_create(t_save)
