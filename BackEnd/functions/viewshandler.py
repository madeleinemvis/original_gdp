from ast import literal_eval

from django.utils.datastructures import MultiValueDictKeyError
from documents.models import Document, Claim
from tweets.models import Tweet, Query
from trends.models import Trend

from .article_sentiments import PredictSentiment
from .dataretrieval import Scraper
from .dbmanager import DbManager


class ViewsHandler:
    db_manager = None
    scraper = Scraper()
    predict_sentiment = PredictSentiment()

    def __init__(self):
        self.db_manager = DbManager()

    def read_docs(self, docs) -> [str]:
        print("docs", docs)
        documents = []
        try:
            docs = literal_eval(docs)
            for d in docs:
                documents.append(docs[d])
        except:
            documents.extend(docs)  # Object is a File.

        documents = self.scraper.downloads(documents)
        doc_list = []
        for d in documents:
            doc_list.append(documents[d])

        return doc_list

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

    @staticmethod
    def set_claim(uid: str, claim: str) -> Claim:
        c_save = Claim(uid=uid, claim=claim)
        return c_save

    @staticmethod
    def set_query(uid: str, query: str) -> Query:
        q_save = Query(uid=uid, query=query)
        return q_save

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

    def save_documents(self, uid: str, content_type: str, documents, predictions_dict):
        print("documents length", len(documents))
        print("predictions length", len(predictions_dict))
        d_save = self.set_documents(uid, content_type, documents, predictions_dict)
        Document.objects.bulk_create(d_save)

    def save_claim(self, uid: str, claim: str):
        c_save = self.set_claim(uid, claim)
        c_save.save()

    def save_query(self, uid: str, query: str):
        q_save = self.set_query(uid, query)
        q_save.save()

    def save_tweets(self, uid: str, tweets):
        t_save = self.set_tweets(uid, tweets)
        Tweet.objects.bulk_create(t_save)

    def save_trends(self, uid: str, econ, health, politics, map_countries, map_trends):
        t_save = self.set_trends(uid, econ, health, politics, map_countries, map_trends)
        Trend.objects.bulk_create(t_save)
