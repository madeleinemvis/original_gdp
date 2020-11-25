from django.conf.urls import url
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/files/', views.FileUploadView.as_view(), name= 'files_list'),]