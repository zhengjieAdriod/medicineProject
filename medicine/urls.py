from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_objects, name='index'),
    url(r'^getObjects/$', views.get_objects, name='index'),  # 测试
    url(r'^getSubjects/$', views.get_subjects, name='subject_list'),
    url(r'^subject/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    #
    url(r'^addSubject/$', views.add_new_subject, name='add_new_subject'),
    url(r'^editSubject/$', views.edit_subject, name='edit_subject'),
    url(r'^deleteSubject/$', views.delete_subject, name='delete_subject'),
    url(r'^praise/$', views.praise, name='praise'),
    url(r'^follower/$', views.follower, name='follower'),
    url(r'^acceptTask/$', views.accept_task, name='accept_task'),
    url(r'^abandonTask/$', views.abandon_task, name='abandon_task'),
    url(r'^addTaskProgress/$', views.add_task_progress, name='add_task_progress'),
    url(r'^updateTaskProgress/$', views.update_task_progress, name='update_task_progress'),
    url(r'^postPic/$', views.post_pic, name='post_pic'),
]
