# -*- coding:utf-8 -*-
from rest_framework import serializers

from medicine.models import Subject, User, Crowd, Task, TaskProgress, Top


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'name', 'telephone', 'age', 'address',)


# class UserFollowerSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = UserFollower
#         fields = ('name', 'telephone', 'age', 'address',)
#
#
# class UserInitiatorSerializer(UserSerializer):
#     class Meta:
#         model = UserInitiator
#         fields = ('name', 'telephone', 'age', 'address',)


class CrowdSerializer(serializers.HyperlinkedModelSerializer):
    # category = CategorySerializer(many=True, read_only=True)#many=True表示category字段的值为数组
    crowd_providers = UserSerializer(many=True, read_only=True)  # 多对多

    class Meta:
        model = Crowd
        fields = ('pk', 'crowd_funding', 'crowd_progress', 'crowd_providers',)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    task_executors = UserSerializer()

    class Meta:
        model = Task
        fields = ('pk', 'task_outline', 'task_deadline', 'task_executors', 'task_start_time', 'task_state',)


class TaskProgressSerializer(serializers.HyperlinkedModelSerializer):
    task = TaskSerializer()

    class Meta:
        model = TaskProgress
        fields = ('pk', 'task', 'des', 'path', 'task_progress_time', 'created_time',)


class TopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Top
        fields = ('is_top', 'top_time',)


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    initiator = UserSerializer()
    task = TaskSerializer()
    crowd = CrowdSerializer()
    followers = UserSerializer(many=True, read_only=True)  # 多对多
    top = TopSerializer()

    class Meta:
        model = Subject
        fields = ('pk', 'initiator', 'followers', 'origin_from', 'title', 'describe', 'content', 'doctor_type',
                  'doctor_address', 'disease_type', 'task', 'crowd', 'created_time', 'praise', 'top')
