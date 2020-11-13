# file for handling API, left blank for now
import pymongo


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

    # Deletes any record that holds true to the query
    def delete_tuple(self, collection, query):
        try:
            self.database[collection].delete_many(query)
        except NoCollectionsError():
            print("No Object, %s,  Found in Collection, %", query, collection)

    # Example values passed in ("WebURLs", "body" "vaccin*"))
    def find_documents(self, collection, column, query_text):
        query = {column: {"$regex": query_text}}
        try:
            documents = self.database[collection].find(query)
            return documents
        except NoObjectsError:
            print("No Objects Found in Collections %s", collection)

    # Returns all documents of a specific collection
    def get_all_documents(self, collection: str):
        try:
            return self.database[collection].find({})
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
        except NoObjectsError:
            print("No Objects Found in Collections %s", collection)
        cleaned_tokens = []
        for tokens in ini_list:
            res = tokens['cleaned_tokens'].strip('][').split(', ')
            cleaned_tokens.extend(res)

        return cleaned_tokens


class Error(Exception):
    """Base class for other exceptions"""
    pass


class NoObjectsError(Error):
    """No Documents Found in Collection"""
    pass


class NoCollectionsError(Error):
    """No Collections in Database"""
