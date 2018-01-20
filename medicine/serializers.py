# -*- coding:utf-8 -*-
from rest_framework import serializers

from medicine.models import Subject


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('pk', 'name', 'content', 'type', 'created_time')
