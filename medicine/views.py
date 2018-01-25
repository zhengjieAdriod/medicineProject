from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404  # 用来渲染html

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


# 分页
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_subjects(request):
    page_size = 0
    page_num = 0
    total_page = 0

    try:
        subjects = Subject.objects.all()
        disease_type = request.GET.get("disease")  # 疾病名称
        if disease_type is not None:  # 疾病分类
            subjects = subjects.filter(disease_type=disease_type)
        page = request.GET.get("page")
        if page is not None:  # 分页
            paginator = Paginator(subjects, 1)  # 每页显示 2 条数据
            page_size = paginator.per_page  # 每页几条数据
            total_page = paginator.num_pages  # 一共多少页数据
            subjects = paginator.page(page)
        subjects_serializer = SubjectSerializer(subjects, many=True)
        return Response({"code": "200", "page_size": page_size, "page_num": page_num, "total_page": total_page,
                         "subject_list": subjects_serializer.data})
    except PageNotAnInteger:
        return Response({"code": "400", "error_msg": "访问出错"})
    except EmptyPage:
        return Response({"code": "400", "error_msg": "该页数据为空"})


@api_view(['GET'])
@permission_classes((AllowAny,))
def detail(request, pk):
    subject_json = {}
    subjects = Subject.objects.filter(pk=pk)
    if len(subjects) > 0:
        subjects_serializer = SubjectSerializer(subjects[0], many=False)
        subject_json = subjects_serializer.data
    return Response({"code": "200", "subject": subject_json})
