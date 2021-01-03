from django.conf.urls import url
from documents import views

urlpatterns = [
    url(r'^api/documents/upload$', views.upload_documents),
    url(r'^api/documents/suggest$', views.suggest_urls),
    url(r'^api/documents/document_list$', views.document_list),
    url(r'api/documents/wordcloud$', views.keywords_wordcloud),
    url(r'api/documents/freq$', views.document_frequency),
]