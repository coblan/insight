from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$',views.home),
    url(r'^home/', views.home),
    url(r'^nd/(.+)',views.insight_engine_view)
    #url(r'^model/(.*)/$',views.model_render_views,name='model')
]