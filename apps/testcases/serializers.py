# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import validators

from .models import Testcases
from interfaces.models import Interfaces
from projects.models import Projects
from apps.interfaces.serializers import InterfacesModelSerializer
from utils import common,validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project=serializers.StringRelatedField(label='所属项目',help_text='所属项目',read_only=True)
    pid=serializers.IntegerField(label='所属项目id',help_text='所属项目id',write_only=True,validators=[validates.is_exist_project_id])
    iid=serializers.IntegerField(label='所属接口id',help_text='所属接口id',write_only=True,validators=[validates.is_exist_project_id])
    class Meta:
        model = Interfaces
        fields = ('iid', 'name','pid','project')
        extra_kwargs = {
            'name': {
                'read_only': True,
            }
        }


    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid,project_id=pid).exist():
            raise serializers.ValidationError('所属项目id与接口id不匹配')



class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label="所属项目及接口信息",help_text="所属项目及接口信息")
    class Meta:
        model = Testcases
        exclude = ('update_time','create_time',)

        extra_kwargs = {
            # 'include':{
            #     'required':True,
            # },
            'request':{
                'write_only':True,
            }
        }

    def create(self, validated_data):
        iid=validated_data.pop("interface").get("iid")
        validated_data['interface_id']=iid
        return super().create(validated_data)

    def update(self, instance, validated_data):
        iid = validated_data.pop("interface").get("iid")
        validated_data['interface_id'] = iid
        return super().update(instance, validated_data)


'''
class ProjectsNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('id', 'name')


class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ('interfaces', )


class InterfacesByProjectIdModelSerializer1(serializers.ModelSerializer):
    # interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'name')
'''