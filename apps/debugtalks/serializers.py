# -*- coding: utf-8 -*-

from rest_framework import serializers

from debugtalks.models import DebugTalks

from utils import common


# 使用模型序列化器类：简化序列化器类中字段的创建
class DebugTalksModelSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        # model = DebugTalks
        # exclude=("update_time","create_time","debugtalk")
        model = DebugTalks
        exclude = ('create_time', 'update_time')
        read_only_fields = ('name', 'project')

        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }


