from django.conf.urls import url 
from trends import views
 
urlpatterns = [
    url(r'^api/trends$', views.tweets_list),
    url(r'^api/trends/freq$', views.tweet_frequency),
    url(r'^api/trends/geo$', views.tweets_geo),
    url(r'^api/trends/sentiment_scatter$', views.sentiment_scatter)
]