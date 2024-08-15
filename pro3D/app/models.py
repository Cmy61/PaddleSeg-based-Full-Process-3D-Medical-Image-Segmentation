from django.db import models
from operator import mod
from pyexpat import model
from statistics import mode
import datetime
from django.contrib.auth.models import AbstractUser,User
from django.utils import timezone
# Create your models here.
# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)# 自动增长，主键
#     name=models.CharField(max_length=30)
#     gender=models.CharField(max_length=5)
#     age=models.IntegerField()
#     phonenumber=models.CharField(max_length=30)
#     address=models.CharField(max_length=100)
# class Medical_infor(models.Model):
#     medical_id=models.AutoField(primary_key=True)
#     storeName=models.CharField(max_length=100)
#     userName=models.CharField(max_length=30,default='John')
#     # user=models.ForeignKey(User, on_delete=models.CASCADE)#参数可以指定删除用户时与之相关的医疗记录也会被删除。


class User(models.Model):
    # user_id = models.CharField(max_length=50, unique=True,default='1',primary_key=True)
    user_id = models.AutoField(primary_key=True)
    # 用户ID，唯一性约束
    user_account=models.CharField(max_length=50,default='zhangsan')
    #账户
    user_password=models.CharField(max_length=20,default='123456')


class Project(models.Model):
    project_id = models.AutoField(primary_key=True,unique=True)
    # 项目ID，唯一性约束
    project_name = models.CharField(max_length=100)
    # 项目名
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 项目和用户的关系是一个用户对应n个项目，外键指向用户模型
    build_time=models.DateTimeField(default=timezone.now())
    #auto_now_add=True创建时自动填写，不需要手动修改
    remark=models.TextField()


class CTSet(models.Model):
    # CT集合ID，唯一性约束
    set_id = models.AutoField( unique=True,primary_key=True)
    # CT集合名
    set_name = models.CharField(max_length=100)
    # CT集合目录
    directory = models.CharField(max_length=200)
    # 上传后临时存放的路径
    original_path = models.CharField(max_length=200)
    # nii文件路径，模型处理前，原文件
    nii_path = models.CharField(max_length=200)
    # label文件路径
    label_path = models.CharField(max_length=200)
        # 被处理后的nii
    nii_after_path=models.CharField(max_length=200)
 # STL文件目录
    stl_directory = models.CharField(max_length=200)
    # CT集合与项目是多对多关系ManyToManyField
    projects = models.ManyToManyField(Project)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    build_time=models.DateTimeField(default=timezone.now())
    #auto_now_add=True创建时自动填写，不需要手动修改
    remark=models.TextField()



class Label(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.IntegerField()
    # 标签，整数
    organ_name = models.CharField(max_length=100)
    # 器官名
    # color = models.CharField(max_length=50)
    # # 颜色，字符串类型
    r = models.IntegerField()
    # 红色通道
    g = models.IntegerField()
    # 绿色通道
    b = models.IntegerField()
    # 蓝色通道
    transparency = models.FloatField()
    # 透明度，浮点数类型，范围0-1
    volume = models.FloatField(default=0)
    # 体积(立方厘米)
    visible = models.BooleanField()
    # 可见性，布尔类型
    stl_path = models.CharField(max_length=200)
    # 对应的STL文件路径
    ct_set = models.ForeignKey(CTSet, on_delete=models.CASCADE,default=1)
    # CT集合和标签是1对n的关系，外键指向CTCollection模型弱实体集
    class Meta:
        unique_together = ('ct_set', 'label')
        # primary_key = models.CompositeKey('ct_set', 'label')
    #Django不支持复合主键。您可以使用
# Meta.unique_together
# 创建单个复合唯一键。