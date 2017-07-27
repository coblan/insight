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
#from user_admin import urls as user_urls
#from user_admin import views as user_views

from helpers.director import login_url 
from helpers.msic.ckeditor import upload_image

from helpers.face import urls as face_urls
from helpers.director import views as director_views

from helpers.dev import urls as dev_urls
from django.views.i18n import javascript_catalog

from hello.engin_proxy import InsightEngine ,MobileEngine,F7Engine

from helpers.case.organize import urls as organize_urls
from helpers.case.work import urls as work_urls
from django.views.generic import RedirectView 
urlpatterns = [
    
    url(r'^accounts/',include(login_url)),


    url(r'wx/home.wx',RedirectView.as_view(url='http://192.168.1.101:8000/home')),

    url(r'pc/([\w\.]+)/?$',InsightEngine.as_view(),name=InsightEngine.url_name),
    url(r'wx/([\w\.]+)/?$',MobileEngine.as_view(),name=MobileEngine.url_name),
    url(r'f7/([\w\.]+)/?$',F7Engine.as_view(),name=F7Engine.url_name),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',hello_view.home),
    #url(r'hello/',include(hello_urls)),
    
    #url(r'user/',include(user_urls),name='user_admin'),
    
    #url(r'^_department/?$',user_views.manage_department),
    
    url(r'^_face/', include(face_urls)),
    url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^_ajax/?$',director_views.ajax_views), 
    url(r'^_download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'),
    url(r'^_f7_iframe/?$',director_views.f7_frame_wraper),
    
    url(r'^dev/',include(dev_urls)),
    url(r'^jsi18n/$', javascript_catalog, name='js-tr'),
    
    url(r'^orgnize/',include(organize_urls)),
    url(r'^work/',include(work_urls)),
    
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)