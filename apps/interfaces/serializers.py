# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/7/1 20:14 
  @Auth : 可优
  @File : serializers.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import serializers
from rest_framework import validators

from .models import Interfaces
from projects.models import Projects
# from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
class InterfacesModelSerializer(serializers.ModelSerializer):
    # a.会将父表的主键id值作为返回值
    # projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
    # b.会将父表对应对象的__str__方法的结果返回
    # projects = serializers.StringRelatedField()
    # c.会将父表对应对象的某个字段的值返回
    # projects = serializers.SlugRelatedField(slug_field='leader', read_only=True)
    # d.可以将某个序列化器对象定义为字段，支持Field中的所有参数
    # projects1 = ProjectsModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = Interfaces
        # fields = ('id', 'name', 'leader', 'tester', 'programmer', 'create_time', 'update_time', 'email')
        fields = '__all__'

