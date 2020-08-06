# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import validators

from interfaces.models import Interfaces
from projects.models import Projects
from configures.models import Configures
from testcases.models import Testcases

from utils import common
# from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
class InterfacesModelSerializer(serializers.ModelSerializer):
    # a.会将父表的主键id值作为返回值
    project_id = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
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
        project=validated_data.pop('project_id')
        validated_data["project_id"]=project.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project.id

        return super().update(instance, validated_data)

class ConfiguresNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name',)
        # fields = "__all__"

class ConfiguresByInterfacesIdModelSerializer(serializers.ModelSerializer):
    configures = ConfiguresNamesModelSerializer(label='接口所属配置id和name',many=True, read_only=True)

    class Meta:
        model =  Interfaces
        fields = ('configures', )

class TestcasesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')

class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
    testcases = TestcasesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('testcases', )