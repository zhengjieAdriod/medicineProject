from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_objects, name='index'),
    url(r'^getObjects/$', views.get_objects, name='index'),
]
