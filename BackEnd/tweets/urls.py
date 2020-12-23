from django.conf.urls import url 
from BackEnd.tweets import views
 
urlpatterns = [
    url(r'^api/tweets$', views.tweets_list),
    url(r'^api/tweets/freq$', views.tweet_frequency),
    url(r'^api/tweets/geo$', views.tweets_geo),
    url(r'^api/tweets/sentiment_scatter$', views.sentiment_scatter),
    url(r'^api/tweets/sentiment_pie_chart$', views.sentiment_pie_chart)
]