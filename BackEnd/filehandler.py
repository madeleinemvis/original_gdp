from dbmanager import DbManager
import sys
sys.path.append('../')
from functions.dataretrieval import Scraper


class FileHandler:
    ROOT_DIR = None
    db_manager = None

    def __init__(self):
        self.db_manager = DbManager()

    def read_docs(self, docs: [str]):
        documents = []
        for d in docs:
            documents.append(Scraper.get_data_from_source(d))
        return documents
