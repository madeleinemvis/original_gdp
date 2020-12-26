from django.conf.urls import url 
from trends import views
 
urlpatterns = [
    url(r'^api/trends/egauge$', views.econ_gauge),
    url(r'^api/trends/ebar$', views.econ_bar),
    url(r'^api/trends/hgauge$', views.health_gauge),
    url(r'^api/trends/hbar$', views.health_bar),
    url(r'^api/trends/pgauge$', views.politics_gauge),
    url(r'^api/trends/pbar$', views.politics_bar),
]