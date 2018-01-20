from django.shortcuts import render  # 用来渲染html

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from medicine.models import Subject
from medicine.serializers import SubjectSerializer


# 两个注解都与rest_framework有关

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_objects(request):
    subjects = Subject.objects.all()
    subject_list = Subject.objects.filter(pk=2)  # 默认从1开始, filter返回的是列表
    subject_serializer = SubjectSerializer(subject_list[0], many=False)  # 第一个参数是对象,而不是列表
    subjects_serializer = SubjectSerializer(subjects, many=True)
    return Response({"code": "200", "subject": subject_serializer.data, "subjects": subjects_serializer.data})
