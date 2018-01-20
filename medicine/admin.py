from django.contrib import admin

# Register your models here.
from medicine.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'type', 'created_time']


admin.site.register(Subject, SubjectAdmin)
