# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework import validators

from .models import Configures
from projects.models import Projects
from configures.models import Configures

from utils import common
# from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
class ConfiguresModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        exclude=("update_time",)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt(),
            },
        }

