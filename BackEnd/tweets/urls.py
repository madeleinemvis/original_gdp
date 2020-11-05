from django.conf.urls import url 
from tweets import views
 
urlpatterns = [
    url(r'^api/tweets$', views.tweets_list),
    url(r'^api/tweets/geo$', views.tweets_geo)
]