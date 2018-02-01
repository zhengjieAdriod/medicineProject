from django.contrib import admin

# Register your models here.
from medicine.models import Subject, User, Task, Crowd, Top, TaskProgress


# 用户
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


# # 话题发起者
# class UserInitiatorAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'name']
#
#
# # 话题关注者
# class UserFollowerAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'name']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title','initiator', 'origin_from', 'doctor_type',
                    'doctor_address', 'disease_type', 'task', 'crowd', 'created_time', 'praise', 'top']


class TaskProgressInline(admin.StackedInline):
    model = TaskProgress
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ['pk', 'task_executors', 'task_start_time', 'task_deadline', 'task_state']
    inlines = [TaskProgressInline]  # 必须是lines


class CrowdAdmin(admin.ModelAdmin):
    list_display = ['pk', 'crowd_funding', 'crowd_progress']


class TopAdmin(admin.ModelAdmin):
    list_display = ['is_top', 'top_time']


admin.site.register(Subject, SubjectAdmin)
# admin.site.register(UserInitiator, UserInitiatorAdmin)
# admin.site.register(UserFollower, UserFollowerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Crowd, CrowdAdmin)
admin.site.register(Top, TopAdmin)
admin.site.site_header = 'Medicine系统管理'
admin.site.site_title = 'medicine'
