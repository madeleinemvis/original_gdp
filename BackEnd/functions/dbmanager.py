from ast import literal_eval

import pymongo


# Handles all interactions with the database
class DbManager:
    database = None

    def __init__(self):
        # Client instantiation with the MongoDB Client
        self.client = pymongo.MongoClient(
            "mongodb+srv://gdp:gdp@propaganda.m00hm.mongodb.net/Trilateral?retryWrites=true&w=majority")
        # Sets the database to our Trilateral Database in the MongoDB Client
        self.database = self.client.Trilateral

    # Deletes an entire collection
    def drop_collections(self):
        try:
            self.database['documents_document'].drop()
            self.database['documents_claim'].drop()
            self.database['documents_graph'].drop()
            self.database['tweets_tweet'].drop()
            self.database['tweets_query'].drop()
            self.database['trends_trend'].drop()

        except pymongo.errors.PyMongoError:
            print("Collection not found Found in Database")

    # Returns all documents of a specific collection
    def get_all_documents(self, uid: str):
        try:
            return list(self.database['documents_document'].find({"uid": uid}))
        except pymongo.errors.PyMongoError:
            print("No Collection Documents_Document,  Found in Database")

    # Returns the number of documents in the collection under the specified uid
    def count_all_documents(self, uid: str):
        try:
            return self.database['documents_document'].find({"uid": uid}).count()
        except pymongo.errors.PyMongoError:
            print("Returns no documents, uid %s,  Found in Database", uid)

    # Returns the number of tweets in the collection under the specified uid
    def count_all_tweets(self, uid: str):
        try:
            return self.database['tweets_tweet'].find({"uid": uid}).count()
        except pymongo.errors.PyMongoError:
            print("Returns no tweets, uid %s,  Found in Database", uid)

    # Returns a list of cleaned tokens from all the Documents under the specified UID
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

    # Returns all the text-bodies from each Document under the specified UID
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

    # Returns all Tweets under the specified UID
    def get_all_tweets(self, uid: str):
        try:
            ini_list = list(self.database['tweets_tweet'].find({"uid": uid}))
            tweets = []
            for t in ini_list:
                tweets.append(
                    dict(uid=t['uid'], screen_name=t['screen_name'], created_at=t['created_at'], text=t['text'],
                         favorite_count=t['favorite_count'],
                         retweet_count=t['retweet_count'], user_location=t['user_location'],
                         sentiment=t['sentiment']))
            return ini_list
        except pymongo.errors.PyMongoError:
            print("No Collection, Tweets_tweet Found in Database")

    # Returns a list of html_links from each Document under the specified UID
    def get_all_html_links(self, uid: str):
        try:
            ini_list = list(self.database['documents_document'].find({"uid": uid},
                                                                     {"_id": 0, "html_links": 1}))
            html_links = []
            for html_link in ini_list:
                res = literal_eval(html_link['html_links'])
                html_links.extend(res)

            return html_links
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Documents_document", uid)

    # Returns a claim under the specified UI
    def get_claim(self, uid: str):
        try:
            c_result = self.database['documents_claim'].find({"uid": uid},
                                                             {"_id": 0, "claim": 1})
            claim = c_result[0]['claim']
            return claim
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Documents_claim", uid)

    # Returns a query under the specified UID
    def get_query(self, uid: str):
        try:
            q_result = self.database['tweets_query'].find({"uid": uid},
                                                          {"_id": 0, "query": 1})
            query = q_result[0]['query']
            return query
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Tweets_Query", uid)

    # Returns all causal data with a specified UID
    def get_causal(self, uid: str):
        try:
            causal = self.database['trends_trend'].find({"uid": uid})
            causal_item = causal[0]
            return causal_item
        except pymongo.errors.PyMongoError:
            print("No Objects, UID: %s,  Found in Collection, Trends_trend", uid)
