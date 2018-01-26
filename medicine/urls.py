from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_objects, name='index'),
    url(r'^getObjects/$', views.get_objects, name='index'),
    url(r'^getSubjects/$', views.get_subjects, name='subject_list'),
    url(r'^subject/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # add_new_subject
    url(r'^addSubject/$', views.add_new_subject, name='add_new_subject'),
]
