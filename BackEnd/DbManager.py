# file for handling API, left blank for now
import pymongo


class DbManager:
    database = None

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://gdp:gdp@propaganda.m00hm.mongodb.net/Trilateral?retryWrites=true&w=majority")
        self.database = self.client.Trilateral
        self.drop_collection('tweets_tweet')

    # Inserts a single document into a specified collection
    def insert_one(self, collection, document):
        self.database[collection].insert_one(document)

    # Inserts a list of documents (documents must be separate dictionaries) into a specified collection
    def insert_many(self, collection, document_list):
        print(collection, document_list)
        self.database[collection].insert_many(document_list)

    # Deletes an entire collection
    def drop_collection(self, collection):
        self.database[collection].drop()
        response = self.database.drop_collection(collection)
        print('\n', 'drop_collection() response: ', response)

    # Deletes any record that holds true to the query
    def delete_tuple(self, collection, query):
        self.database[collection].delete_many(query)

    # Example values passed in ("WebURLs", "body" "vaccin*"))
    def find_documents(self, collection, column, query_text):
        query = {column: {"$regex": query_text}}
        documents = self.database[collection].find(query)
        return documents

    def count_documents(self, collection, column, query_text):
        query = {column: {"$regex": query_text}}
        return self.database[collection].count_documents(query)

    # Returns all documents of a specific collection
    def get_all_documents(self, collection_name: str):
        return self.database[collection_name].find()

    def get_all_collections(self):
        return self.database.getCollectionNames
