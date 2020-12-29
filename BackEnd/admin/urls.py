"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from admin import settings
from django.views.generic import TemplateView
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    url(r'^', include('documents.urls')),
    url(r'^', include('tweets.urls')),
    url(r'^', include('trends.urls'))
]

# If the web-page is refreshed.
react_routes = getattr(settings, 'REACT_ROUTES', [])
for route in react_routes:
    urlpatterns += [
        path('{}'.format(route), TemplateView.as_view(template_name='frontend/index.html'))
    ]

