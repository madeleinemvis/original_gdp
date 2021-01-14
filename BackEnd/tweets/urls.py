from django.conf.urls import url
from tweets import views

# All Tweet related URLs that the web-page can call, with the respective function to be called in tweets/views.py
urlpatterns = [
    url(r'^api/tweets$', views.tweets_list),
    url(r'^api/tweets/tweet_query', views.tweet_query),
    url(r'^api/tweets/freq$', views.tweet_frequency),
    url(r'^api/tweets/geo$', views.tweets_geo),
    url(r'^api/tweets/sentiment_scatter$', views.sentiment_scatter),
    url(r'^api/tweets/sentiment_pie_chart$', views.sentiment_pie_chart),
    url(r'^api/tweets/tweet_summary$', views.tweet_summary),
    url(r'^api/tweets/date_impact_bar$', views.date_impact_bar)
]
