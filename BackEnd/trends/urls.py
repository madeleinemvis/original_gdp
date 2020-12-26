from django.conf.urls import url 
from trends import views
 
urlpatterns = [
    url(r'^api/trends/econ_gauge$', views.econ_gauge),
    url(r'^api/trends/econ_bar$', views.econ_bar),
    url(r'^api/trends/health_gauge$', views.health_gauge),
    url(r'^api/trends/health_bar$', views.health_bar),
    url(r'^api/trends/politics_gauge$', views.politics_gauge),
    url(r'^api/trends/politics_bar$', views.politics_bar),
]