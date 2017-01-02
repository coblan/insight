"""insight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from hello import urls as hello_urls
from hello import views as hello_view
from user_admin import urls as user_urls
from helpers.director import urls as director_urls
urlpatterns = [
    
    url(r'^accounts/',include(director_urls)),
    url(r'^d/',include(director_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',hello_view.home),
    #url(r'hello/',include(hello_urls)),
    
    url(r'user/',include(user_urls),name='user_admin')
]
