# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import validators

from .models import Projects
from interfaces.models import Interfaces
from debugtalks.models import DebugTalks
from apps.interfaces.serializers import InterfacesModelSerializer
from utils import common


class InterfacesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt(),
            },

        }

    def create(self, validated_data):
        # 在创建项目时，同时创建一个空的debugtalk.py文件
        project = super().create(validated_data)
        DebugTalks.objects.create(project=project)
        return project


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