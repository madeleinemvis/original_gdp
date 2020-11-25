import os
import shutil
import zipfile
from dbmanager import DbManager

from django.utils.datastructures import MultiValueDictKeyError
from documents.models import Document, Claim


from functions.dataretrieval import Scraper


class FileHandler:
    ROOT_DIR = None
    db_manager = None
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    scraper = Scraper()

    def __init__(self):
        self.db_manager = DbManager()

    def read_docs(self, docs: [str]):
        documents = []
        for d in docs:
            documents.append(self.scraper.get_data_from_source(d))
        return documents

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

    def read_zip_file(self, uid: str, files):
        relative_zip_dir = 'temp/{}.zip'.format(uid)
        temp_upload_dir = '{}/{}'.format(self.ROOT_DIR, relative_zip_dir)
        files.save(temp_upload_dir)

        # Extract zip file
        self.extract_zip_files(uid, relative_zip_dir)

        # Convert files into Documents
        self.read_files(uid)

        # Delete files
        self.delete_temp_files(uid, relative_zip_dir)

    @staticmethod
    def extract_zip_files(uid: str, relative_zip_dir: str):
        extract_path = 'temp/{}/'.format(uid)
        with zipfile.ZipFile(relative_zip_dir) as zip_ref:
            zip_ref.extractall(extract_path)

    def read_files(self, uid: str):
        documents = []
        extract_path = 'temp/{}/'.format(uid)
        for filename in os.listdir(extract_path):
            with open(extract_path + filename, 'rb') as f:
                documents.append(self.scraper.get_data_from_source(extract_path + filename))

        return documents

    @staticmethod
    def delete_temp_files(uid: str, relative_zip_dir: str):
        os.remove(relative_zip_dir)
        extract_path = 'temp/{}/'.format(uid)
        shutil.rmtree(extract_path)

    @staticmethod
    def get_objects_from_request(request, request_form):
        uid = request_form.cleaned_data['uid']
        claim = request_form.cleaned_data['claim']
        document_urls = request_form.cleaned_data['urls']
        document_pdfs = request_form.cleaned_data['pdfs']
        zip_file = None
        try:
            zip_file = request.FILES['files']
        except MultiValueDictKeyError:
            pass
        return uid, claim, document_urls, document_pdfs, zip_file

    def save_documents(self, uid: str, content_type: str, documents):
        d_save = self.set_documents(uid, content_type, documents)
        Document.objects.bulk_create(d_save)

    def save_claim(self, uid: str, claim: str):
        c_save = self.set_claim(uid, claim)
        c_save.save()
