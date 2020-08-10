from rest_framework import serializers
from projects.models import Projects
from interfaces.models import Interfaces

def is_exist_project_id(value):
    if not Projects.objects.filter(id=value).exists():
        raise serializers.ValidationError('项目id不存在')

def is_exist_interface_id(value):
    if not Interfaces.objects.filter(id=value).exists():
        raise serializers.ValidationError('接口id不存在')