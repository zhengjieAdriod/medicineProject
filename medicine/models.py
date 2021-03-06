import time
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible


# 用户(可以拥有多个角色)(todo 用户之间如何关注)
@python_2_unicode_compatible  # 兼容python2
class User(models.Model):
    name = models.CharField(max_length=70, blank=True)
    telephone = models.CharField(max_length=70, blank=True)
    age = models.IntegerField(blank=True, default=20)
    address = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return "用户:" + str(self.pk) + self.name


# @python_2_unicode_compatible  # 因为继承于User,因此该表中所以数据都包含在User表中
# class UserFollower(User):
#     def __str__(self):
#         return "用户:" + self.name
#
#
# @python_2_unicode_compatible  # 因为继承于User,因此该表中所以数据都包含在User表中
# class UserInitiator(User):
#     def __str__(self):
#         return "用户:" + self.name


# 众筹实体
@python_2_unicode_compatible  # 兼容python2
class Crowd(models.Model):
    # 众筹金额
    crowd_funding = models.CharField(max_length=70, blank=True)
    # 众筹进度(完成金额)
    crowd_progress = models.CharField(max_length=70, blank=True)
    # 金额提供者(所有注册用户)(多对多)
    crowd_providers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "众筹金额:" + self.crowd_funding


# 任务实体
@python_2_unicode_compatible  # 兼容python2
class Task(models.Model):
    STATE_CHOICES = (("01", "待执行"), ("02", "执行中"), ("03", "执行完成"), ("04", "失效"))
    # 任务概要
    task_outline = models.CharField(max_length=100, blank=True)
    # 任务限时
    task_deadline = models.CharField(max_length=70, blank=True)
    # 众筹执行者(暂时为一人可以多任务,而不是多人对应多任务)
    task_executors = models.ForeignKey(User, null=True, blank=True)
    # 任务开始时间
    task_start_time = models.DateTimeField(auto_now_add=True)
    # 任务状态
    task_state = models.CharField(max_length=70, blank=True, choices=STATE_CHOICES, default="01")

    def __str__(self):
        return str(self.pk) + ", 任务概要:" + self.task_outline


# 任务进展
@python_2_unicode_compatible  # 兼容python2
class TaskProgress(models.Model):
    # 一个任务对应多个任务过程
    task = models.ForeignKey(Task, null=True, blank=True)
    # 执行任务记录描述
    des = models.TextField(blank=True, default="执行任务记录描述")
    # 任务执行中所拍摄的图片
    path = models.FileField(upload_to='image/', blank=True)
    # 任务进展时间
    task_progress_time = models.DateTimeField(auto_now_add=True)
    # 任务首次创建的时间
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "执行任务记录描述:" + self.des

    class Meta:
        ordering = ['-created_time']


@python_2_unicode_compatible  # 兼容python2
class Top(models.Model):
    is_top = models.BooleanField(default=False)
    top_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "该话题是否被置顶:" + str(self.is_top)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    t = time.time()
    time_str = str(round(t * 1000))  # 毫秒时间戳
    return 'user_{0}_{1}/{2}'.format(str(instance), time_str, filename)


# 话题
@python_2_unicode_compatible  # 兼容python2
class Subject(models.Model):
    TYPE_CHOICES = (("01", '中'), ("02", '西'),)
    FROM_CHOICES = (("01", "亲朋介绍"), ("02", "网络"), ("03", "电视广告"), ("04", "其他途径"))
    # 话题发起人(一对多)
    # 如果有多个ManyToManyField指向同一个Model,这样反向查询FOO_set的时候就无法弄清是哪个ManyToManyField字段了,可以禁止反向关系:
    # http://www.cnblogs.com/linxiyue/p/3667418.html
    # initiator = models.ForeignKey(User, null=True, blank=True, related_name='u+')
    initiator = models.ForeignKey(User, null=True, blank=True, related_name='subjects_for_initiator')
    # 话题关注者(多对多)
    followers = models.ManyToManyField(User, blank=True, related_name='subjects_for_followers')
    # 话题来源途径
    origin_from = models.CharField(max_length=70, blank=True, choices=FROM_CHOICES)
    # 话题标题
    title = models.CharField(max_length=100, blank=True)
    # 话题描述
    describe = models.TextField(blank=True)
    # 话题详细内容(html)
    content = models.TextField(blank=True)
    # 医家类别
    doctor_type = models.CharField(max_length=70, blank=True, choices=TYPE_CHOICES)
    # 医家地址
    doctor_address = models.CharField(max_length=100, blank=True)
    # 求治疾病类别(糖尿病,腰间盘突出)
    disease_type = models.CharField(max_length=70, blank=True)
    # 任务实体
    task = models.OneToOneField(Task, null=True, blank=True)
    # 众筹实体
    crowd = models.OneToOneField(Crowd, null=True, blank=True)
    # 话题发起时间
    created_time = models.DateTimeField(auto_now_add=True)

    # 点赞
    praise = models.IntegerField(blank=True, default=0)
    # 顶置
    top = models.ForeignKey(Top, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

        # 自定义 get_absolute_url 方法
        # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('medicine:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']


# 上传的文件实体
@python_2_unicode_compatible  # 兼容python2
class FileBean(models.Model):
    user_post = models.ForeignKey(User, null=True, blank=True)
    # 文件描述
    des = models.TextField(blank=True, default="文件描述")
    post_time = models.DateTimeField(auto_now_add=True)
    # 文件路径upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    path = models.FileField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return str(self.user_post.pk)

    class Meta:
        ordering = ['-post_time']
