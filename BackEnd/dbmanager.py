# file for handling API, left blank for now
import pymongo
from BackEnd.errorhandler import NoObjectsError, NoCollectionsError
from ast import literal_eval


class DbManager:
    database = None

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://gdp:gdp@propaganda.m00hm.mongodb.net/Trilateral?retryWrites=true&w=majority")
        self.database = self.client.Trilateral
        # self.drop_collection('documents_document')

    # Inserts a single document into a specified collection
    def insert_one(self, collection, document):
        try:
            self.database[collection].insert_one(document)
        except NoCollectionsError():
            print("No Collection, %s,  Found in Database", collection)

    # Inserts a list of documents (documents must be separate dictionaries) into a specified collection
    def insert_many(self, collection, document_list):
        try:
            print(collection, document_list)
            self.database[collection].insert_many(document_list)
        except NoCollectionsError():
            print("No Collection, %s,  Found in Database", collection)

    # Deletes an entire collection
    def drop_collection(self, collection):
        try:
            self.database[collection].drop()
            response = self.database.drop_collection(collection)
            print('\n', 'drop_collection() response: ', response)
        except NoCollectionsError():
            print("No Collection, %s,  Found in Database", collection)

    def drop_documents(self, uid: str, collection: str):
        try:
            self.database[collection].remove({"uid": uid})
        except NoObjectsError():
            print("No Objects, UID: %s,  Found in Collection, %", uid, collection)

    # Deletes any record that holds true to the query
    def delete_tuple(self, collection: str, query: str):
        try:
            self.database[collection].delete_many(query)
        except NoCollectionsError():
            print("No Object, %s,  Found in Collection, %", query, collection)

    # Example values passed in ("WebURLs", "body" "vaccin*"))
    def find_documents(self, uid: str, collection: str, query: str):
        try:
            query_uid = ("uid:%s, ".join(query), uid)
            documents = self.database[collection].find({query_uid})
            return documents
        except NoObjectsError:
            print("No Objects, UID: %s,  Found in Collection, %", uid, collection)

    # Returns all documents of a specific collection
    def get_all_documents(self, uid: str, collection: str):
        try:
            return list(self.database[collection].find({"uid": uid}))
        except NoObjectsError():
            print("No Collection, %s,  Found in Database", collection)

    def get_all_collections(self):
        try:
            return self.database.getCollectionNames
        except NoCollectionsError():
            print("No Collections Found in Database")

    def get_all_cleaned_tokens(self, uid: str, collection: str):
        try:
            ini_list = list(self.database[collection].find({"uid": uid},
                                                           {"_id": 0, "cleaned_tokens": 1}))
            cleaned_tokens = []
            for tokens in ini_list:
                res = literal_eval(tokens['cleaned_tokens'])
                cleaned_tokens.extend(res)

            return cleaned_tokens
        except NoCollectionsError:
            print("No Collection, %s,  Found in Database", collection)

    def get_all_main_texts(self, uid: str, collection: str):
        try:
            ini_list = list(self.database[collection].find({"uid": uid},
                                                           {"_id": 0, "text_body": 1}))
            main_text = []
            for text in ini_list:
                main_text.append(text['text_body'])

            return " ".join([text for text in main_text])
        except NoCollectionsError:
            print("No Collection, %s,  Found in Database", collection)

    def get_all_html_links(self, uid: str, collection: str):
        try:
            ini_list = list(self.database[collection].find({"uid": uid},
                                                           {"_id": 0, "html_links": 1}))

            html_links = []
            for html_link in ini_list:
                res = literal_eval(html_link['html_links'])
                html_links.extend(res)

            return html_links
        except NoObjectsError():
            print("No Objects, UID: %s,  Found in Collection, %", uid, collection)
