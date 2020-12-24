from django.conf.urls import url 
from causal import views
 
urlpatterns = [
    url(r'^api/causal$', views.tweets_list),
    url(r'^api/causal/freq$', views.tweet_frequency),
    url(r'^api/causal/geo$', views.tweets_geo),
    url(r'^api/causal/sentiment_scatter$', views.sentiment_scatter)
]