from django.conf.urls import url 
from documents import views 
 
urlpatterns = [ 
    url(r'^api/documents$', views.document_list),
    url(r'^api/documents/(?P<pk>[0-9]+)$', views.document_detail)
]