# file for handling API, left blank for now
import pymongo
from ast import literal_eval


class DbManager:
    database = None

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://gdp:gdp@propaganda.m00hm.mongodb.net/Trilateral?retryWrites=true&w=majority")
        self.database = self.client.Trilateral
        # self.drop_collection('documents_document')
        # self.drop_collection('documents_claim')
        # self.drop_collection('tweets_tweet')

    # Inserts a single document into a specified collection
    def insert_one(self, collection, document):
        try:
            self.database[collection].insert_one(document)
        except pymongo.errors.PyMongoError:
            print("No Collection, %s,  Found in Database", collection)

    # Inserts a list of documents (documents must be separate dictionaries) into a specified collection
    def insert_many(self, collection, document_list):
        try:
            print(collection, document_list)
            self.database[collection].insert_many(document_list)
        except pymongo.errors.PyMongoError:
            print("No Collection, %s,  Found in Database", collection)

    # Deletes an entire collection
    def drop_collection(self, collection):
        try:
            self.database[collection].drop()
            response = self.database.drop_collection(collection)
            print('\n', 'drop_collection() response: ', response)
        except pymongo.errors.PyMongoError:
            print("No Collection, %s,  Found in Database", collection)

    def drop_documents(self, uid: str):
        try:
            self.database['documents_document'].remove({"uid": uid})
            self.database['documents_claim'].remove({"uid": uid})
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Documents_Document", uid)

    # Deletes any record that holds true to the query
    def delete_tuple(self, collection: str, query: str):
        try:
            self.database[collection].delete_many(query)
        except pymongo.errors.PyMongoError:
            print("No Object, %s,  Found in Collection, %s", query, collection)

    # Example values passed in ("WebURLs", "body" "vaccin*"))
    def find_documents(self, uid: str, collection: str, query: str):
        try:
            query_uid = ("uid:%s, ".join(query), uid)
            documents = self.database[collection].find({query_uid})
            return documents
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, %s", uid, collection)

    # Returns all documents of a specific collection
    def get_all_documents(self, uid: str):
        try:
            return list(self.database['documents_document'].find({"uid": uid}))
        except pymongo.errors.PyMongoError:
            print("No Collection Documents_Document,  Found in Database")

    def get_all_collections(self):
        try:
            return self.database.getCollectionNames
        except pymongo.errors.PyMongoError:
            print("No Collections Found in Database")

    def get_all_cleaned_tokens(self, uid: str):
        try:
            ini_list = list(self.database['documents_document'].find({"uid": uid},
                                                                     {"_id": 0, "cleaned_tokens": 1}))
            cleaned_tokens = []
            for tokens in ini_list:
                res = literal_eval(tokens['cleaned_tokens'])
                cleaned_tokens.extend(res)

            return cleaned_tokens
        except pymongo.errors.PyMongoError:
            print("No Collection, Documents_Document Found in Database")

    def get_all_main_texts(self, uid: str):
        try:
            ini_list = list(self.database['documents_document'].find({"uid": uid},
                                                                     {"_id": 0, "text_body": 1}))
            main_text = []
            for text in ini_list:
                main_text.append(text['text_body'])

            return " ".join([text for text in main_text])
        except pymongo.errors.PyMongoError:
            print("No Collection, Documents_document  Found in Database")

    def get_all_tweets(self, uid: str):
        try:
            ini_list = list(self.database['tweets_tweet'].find({"uid": uid}))
            return ini_list
        except pymongo.errors.PyMongoError:
            print("No Collection, Tweets_tweet Found in Database")

    def get_all_html_links(self, uid: str):
        try:
            ini_list = list(self.database['documents_document'].find({"uid": uid},
                                                                     {"_id": 0, "html_links": 1}))
            html_links = []
            for html_link in ini_list:
                res = literal_eval(html_link['html_links'])
                html_links.extend(res)

            return html_links
        except  pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Documents_document", uid)

    def get_claim(self, uid: str):
        try:
            c_result = self.database['documents_claim'].find({"uid": uid},
                                                          {"_id": 0, "claim": 1})
            claim = c_result[0]['claim']
            return claim
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Documents_claim", uid)
