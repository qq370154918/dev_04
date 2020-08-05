# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import validators

from interfaces.models import Interfaces
from projects.models import Projects
from configures.models import Configures

from utils import common
# from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
class InterfacesModelSerializer(serializers.ModelSerializer):
    # a.会将父表的主键id值作为返回值
    project_id = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all(),write_only=True)
    # b.会将父表对应对象的__str__方法的结果返回
    # projects = serializers.StringRelatedField()
    # c.会将父表对应对象的某个字段的值返回
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # d.可以将某个序列化器对象定义为字段，支持Field中的所有参数
    # projects1 = ProjectsModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = Interfaces
        # fields = ('id', 'name', 'leader', 'tester', 'programmer', 'create_time', 'update_time', 'email')
        # fields = '__all__'
        exclude=("update_time",)

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt(),
            },
        }
    def create(self, validated_data):
        projects=validated_data.pop('project_id')
        validated_data["project_id"]=projects.id
        return super().create(validated_data)

class ConfiguresNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name',)
        # fields = "__all__"

class InterfacesByConfigureIdModelSerializer(serializers.ModelSerializer):
    interfaces = ConfiguresNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model =  Interfaces
        fields = ('interfaces', )