from django.conf.urls import include, url
import views
urlpatterns = [
    url(r'^login/',views.login,name='login'),
    url(r'regist/',views.regist_user,name='regist'),
    url(r'^logout/$',views.logout),
    url(r'pswd/',views.change_pswd)
    
]