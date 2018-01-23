from django.shortcuts import render  # 用来渲染html

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from medicine.models import Subject, User
from medicine.serializers import SubjectSerializer, UserSerializer


# 两个注解都与rest_framework有关

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_objects(request):
    subjects = Subject.objects.all()
    subject_list = Subject.objects.filter(pk=2)  # 默认从1开始, filter返回的是列表
    subject = subject_list[0]
    ff = subject.followers  # 拿不到,因为数据库中有中间表(存放关系), 也就是说subject表中根本没有followers字段
    fff = subject.initiator  # 能拿到是因为subject表中存有initiator_id
    subject_serializer = SubjectSerializer(subject, many=False)  # 第一个参数是对象,而不是列表
    subjects_serializer = SubjectSerializer(subjects, many=True)
    sData = subject_serializer.data
    rf = sData.get("followers")  # 可以拿到Subject对象下的list字段(任何字段),因为sData是序列化后的字典
    sDatas = subjects_serializer.data
    return Response({"code": "200", "subject": sData, "subjects": sDatas})
