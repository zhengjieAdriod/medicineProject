import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404  # 用来渲染html

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from medicine.models import Subject, User, Crowd, Task, Top
from medicine.serializers import SubjectSerializer, UserSerializer


# 两个注解都与rest_framework有关
# 测试
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


# 新增话题(任何人)
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_new_subject(request):  # 只是新增主题, 不涉及图片
    try:
        data = request.data
        # 获得文件
        # file_dic = request.FILES.dict()
        res_json = data['res']
        post_dic = json.loads(res_json)  # 反序列化,将json串转为字典
        subject_dic = post_dic["subject"]

        initiator_dic = subject_dic["initiator"]  # 发起者(前提是已经注册登录)
        telephone = initiator_dic["telephone"]
        users_db = User.objects.filter(telephone=telephone)
        user_db = users_db[0]

        crowd_dic = subject_dic["crowd"]  # 众筹参数
        new_crowd = Crowd()
        new_crowd.crowd_funding = crowd_dic["crowd_funding"]
        new_crowd.crowd_progress = crowd_dic["crowd_progress"]
        # new_crowd.crowd_providers = crowd_dic['crowd_providers'] #众筹参与者

        describe_str = subject_dic["describe"]  # 话题描述参数
        disease_type_str = subject_dic['disease_type']  # 疾病类型
        doctor_address_str = subject_dic['doctor_address']  # 医生地址
        doctor_type_str = subject_dic['doctor_type']  # 医生类型
        # followers = []  # 关注者为空列表

        origin_from_str = subject_dic['origin_from']  # 话题来源

        praise = 0  # 点赞数

        task_dic = subject_dic['task']  # 话题的任务
        new_task = Task()
        new_task.task_deadline = task_dic['task_deadline']
        new_task.task_outline = task_dic['task_outline']

        top_dic = subject_dic['top']
        new_top = Top()
        new_top.is_top = top_dic['is_top']
        new_top.top_time = top_dic['top_time']

    except KeyError as e:
        return Response({"code": "400", "errorMsg": e})

    new_subject = Subject()  # 新增话题
    new_subject.initiator = user_db
    new_subject.describe = describe_str
    new_subject.disease_type = disease_type_str
    new_subject.doctor_address = doctor_address_str
    new_subject.doctor_type = doctor_type_str
    new_subject.origin_from = origin_from_str
    new_subject.praise = praise

    new_crowd.save()
    new_subject.crowd = new_crowd  # 一定要先保存new_crowd,再对new_subject.crowd赋值
    new_task.save()
    new_subject.task = new_task
    new_top.save()
    new_subject.top = new_top
    new_subject.save()

    # new_top.subject_set.add(new_subject)

    return Response({"code": "200", "subject": ""})


# 修改话题(话题发起人的权限)
@api_view(['POST'])
@permission_classes((AllowAny,))
def edit_subject(request):
    try:
        data = request.data
        # 获得文件
        # file_dic = request.FILES.dict()
        res_json = data['res']
        post_dic = json.loads(res_json)  # 反序列化,将json串转为字典
        subject_dic = post_dic["subject"]
        subject_pk = subject_dic["pk"]
        subject_dbs = Subject.objects.filter(pk=subject_pk)
        if len(subject_dbs) == 0:
            return Response({"code": "400", "errorMsg": "pk参数有误"})

        subject_db = subject_dbs[0]

        initiator_pk = subject_db.initiator.pk
        initiator_dic = subject_dic['initiator']  # 话题发起人
        if initiator_pk != initiator_dic['pk']:
            return Response({"code": "400", "errorMsg": "只有本话题的发起人才有权限编辑本话题"})

        task_db = subject_db.task
        task_db_state = task_db.task_state  # 任务状态
        if task_db_state != "01":
            return Response({"code": "400", "errorMsg": "话题的任务已经被执行,不可编辑"})
        # 只有话题任务为待执行状态, 则众筹实体和任务实体才可以被编辑
        crowd_db = subject_db.crowd
        crowd_db.crowd_funding = subject_dic['crowd']['crowd_funding']
        crowd_db.crowd_progress = subject_dic['crowd']["crowd_progress"]
        crowd_db.save()
        task_db.task_deadline = subject_dic['task']['task_deadline']
        task_db.task_outline = subject_dic['task']['task_outline']
        task_db.save()

        describe_str = subject_dic["describe"]  # 话题描述参数
        disease_type_str = subject_dic['disease_type']  # 疾病类型
        doctor_address_str = subject_dic['doctor_address']  # 医生地址
        doctor_type_str = subject_dic['doctor_type']  # 医生类型
        origin_from_str = subject_dic['origin_from']  # 话题来源
        praise = 0  # 点赞数
    except KeyError as e:
        return Response({"code": "400", "errorMsg": e})
    subject_db.describe = describe_str
    subject_db.disease_type = disease_type_str
    subject_db.doctor_address = doctor_address_str
    subject_db.doctor_type = doctor_type_str
    subject_db.origin_from = origin_from_str
    subject_db.praise = praise
    subject_db.save()
    return Response({"code": "200", "success": "编辑成功"})


# 删除话题(话题发起人的权限)
@api_view(['GET'])
@permission_classes((AllowAny,))
def delete_subject(request):
    subject_pk = request.GET.get("pk")
    user_pk = request.GET.get("userPk")
    users_db = User.objects.filter(pk=user_pk)
    if len(users_db) == 0:
        return Response({"code": "400", "msg": "删除失败,用户不存在"})
    subjects_db = Subject.objects.filter(pk=subject_pk)
    if len(subjects_db) > 0 and len(users_db) > 0:
        user_db = users_db[0]
        subjects_inited = user_db.subjects_for_initiator.all()  # 当前用户已经发起的主题列表
        subject_db = subjects_db[0]
        if subject_db in subjects_inited:
            user_db.subjects_for_initiator.remove(subject_db)
            subject_db.delete()
            return Response({"code": "200", "msg": "删除完成"})
    return Response({"code": "400", "msg": "删除失败"})


# 对话题点赞 (任何人均有的权限)
# 如: http://127.0.0.1:8000/acceptTask/?pk=16
@api_view(['GET'])
@permission_classes((AllowAny,))
def praise(request):
    subject_pk = request.GET.get("pk")
    subjects_db = Subject.objects.filter(pk=subject_pk)
    if len(subjects_db) > 0:
        subject_db = subjects_db[0]
        subject_db.praise = str(int(subject_db.praise) + 1)
        subject_db.save()
        return Response({"code": "200", "success": "点赞成功", "praise": subject_db.praise})
    return Response({"code": "400", "success": "点赞失败"})


# 关注话题(任何人均有的权限)
# 如: http://127.0.0.1:8000/acceptTask/?pk=16&userPk=6

@api_view(['GET'])
@permission_classes((AllowAny,))
def follower(request):
    subject_pk = request.GET.get("pk")
    user_pk = request.GET.get("userPk")
    users_db = User.objects.filter(pk=user_pk)
    if len(users_db) == 0:
        return Response({"code": "400", "msg": "关注失败,用户不存在"})
    subjects_db = Subject.objects.filter(pk=subject_pk)
    if len(subjects_db) > 0 and len(users_db) > 0:
        user_db = users_db[0]
        subjects_followed = user_db.subjects_for_followers.all()  # 当前用户已经关注的主题列表
        subject_db = subjects_db[0]
        if subject_db in subjects_followed:
            return Response({"code": "200", "msg": "关注失败,不能重复关注同一个主题"})
        user_db.subjects_for_followers.add(subject_db)
        subject_db.save()
        return Response({"code": "200", "msg": "关注成功", "followersCount": subject_db.followers.count()})
    return Response({"code": "400", "msg": "关注失败"})


# 接受话题的任务(任何人均有的权限)
# 如: http://127.0.0.1:8000/acceptTask/?pk=16&userPk=6
# pk是话题的pk,而不是任务的pk
@api_view(['GET'])
@permission_classes((AllowAny,))
def accept_task(request):
    subject_pk = request.GET.get("pk")
    user_pk = request.GET.get("userPk")
    users_db = User.objects.filter(pk=user_pk)
    if len(users_db) == 0:
        return Response({"code": "400", "msg": "接受失败,用户不存在"})
    subjects_db = Subject.objects.filter(pk=subject_pk)

    if len(subjects_db) > 0 and len(users_db) > 0:
        user_db = users_db[0]
        subject_db = subjects_db[0]
        task_db = subject_db.task
        if task_db is None:
            return Response({"code": "400", "msg": "接受失败,任务不存在"})
        users_executing = task_db.task_executors  # 该任务的执行者
        if users_executing is not None:
            return Response({"code": "400", "msg": "接受失败,任务已经在被执行"})
        tasks_accepted = user_db.task_set.all()
        if task_db in tasks_accepted:
            return Response({"code": "400", "msg": "接受失败,不能重复接受同一个任务"})
        task_db.task_state = "02"
        task_db.save()
        user_db.task_set.add(task_db)
        return Response({"code": "200", "msg": "接受成功", "tasks_accepted_count": tasks_accepted.count()})
    return Response({"code": "400", "msg": "接受失败"})


# 放弃话题任务的执行权(任务执行者才有的权限)
# 如: http://127.0.0.1:8000/***/?pk=16&userPk=6
# pk是话题的pk,而不是任务的pk
@api_view(['GET'])
@permission_classes((AllowAny,))
def abandon_task(request):
    subject_pk = request.GET.get("pk")
    user_pk = request.GET.get("userPk")
    users_db = User.objects.filter(pk=user_pk)
    if len(users_db) == 0:
        return Response({"code": "400", "msg": "接受失败,用户不存在"})
    subjects_db = Subject.objects.filter(pk=subject_pk)

    if len(subjects_db) > 0 and len(users_db) > 0:
        user_db = users_db[0]
        subject_db = subjects_db[0]
        task_db = subject_db.task
        if task_db is None:
            return Response({"code": "400", "msg": "任务不存在"})
        users_executing = task_db.task_executors  # 该任务的执行者
        if users_executing is None:
            return Response({"code": "400", "msg": "任务执行者不存在"})
        tasks_accepted = user_db.task_set.all()
        if task_db in tasks_accepted:  # tasks_accepted 中存在该任务时,表明该user是该任务的执行者
            user_db.task_set.remove(task_db)
            task_db.task_executors = None
            task_db.task_state = "01"
            task_db.save()
            return Response({"code": "200", "msg": "放弃任务成功"})
    return Response({"code": "400", "msg": "放弃任务失败"})

    # todo  编辑任务的执行流程(话题发起人的权限)
    # @api_view(['POST'])
    # @permission_classes((AllowAny,))
    # def
