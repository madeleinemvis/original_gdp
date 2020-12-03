import os
import shutil
import zipfile
from ast import literal_eval

from .dbmanager import DbManager

from django.utils.datastructures import MultiValueDictKeyError
from documents.models import Document, Claim


from .dataretrieval import Scraper


class FileHandler:
    ROOT_DIR = None
    db_manager = None
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
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
