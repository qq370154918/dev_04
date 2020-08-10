import re

from rest_framework import serializers
from rest_framework import validators

from .models import Testsuits
from projects.models import Projects
from utils.common import datetime_fmt
from interfaces.models import Interfaces


def validate_include(value):
    # 对入参格式进行校验匹配 [ ]中间一个或多个用,号隔开的1位或者多位数字
    obj = re.match(r"^\[\d+(, \d+)*\]$", value)
    # 如果未匹配到，则说明参数格式非所有元素都为数字的的列表
    if obj is None:
        raise serializers.ValidationError('参数格式有误')
    # 如果匹配到，尽心格式转换（group获取到的是字符串，转换成列表）
    else:
        res = obj.group()
        try:
            data = eval(res)
        except:
            raise serializers.ValidationError('参数格式有误')
        # 遍历列表，如果列表中元素非interfaces表的id，则校验失败并给出对应错误信息
        for item in data:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'update_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'include': {
                'write_only': True,
                'validators': [validate_include]
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().update(instance, validated_data)

class TestsuitsDetailModelSerializer(TestsuitsModelSerializer):
    class Meta:
        model = Testsuits
        fields = ('name', 'project_id', 'include', )

        extra_kwargs = {
            'include': {
                'write_only': False,
            }
        }