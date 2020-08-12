import json
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Configures
from interfaces.models import Interfaces
from .serializers import ConfiguresModelSerializer
from .utils import handel_request_headers,handel_test_data_variables

class ConfiguresViewSet(viewsets.ModelViewSet):
    """
    list:
    获取项目的列表信息

    retrive:
    获取项目详情数据

    create:
    创建项目

    names:
    获取项目名称

    interfaces:
    获取某个项目下的接口名称
    """
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # 获取当前用例的模型类对象
        config_obj = self.get_object()
        # 获取配置所属项目id
        selected_project_id = Interfaces.objects.get(id=config_obj.interface_id).project_id

        # 获取数据库request字段内容
        request_data = json.loads(config_obj.request,encoding='utf-8')
        print(request_data)
        config_data = request_data.get('config')
        config_request_data=config_data.get('request')

        datas = {
            "author": config_obj.author,
            "configure_name": config_obj.name,
            "selected_interface_id": config_obj.interface_id,
            "selected_project_id": selected_project_id,
            "header": handel_request_headers(config_request_data.get('headers')),
            "globalVar": handel_test_data_variables(config_data,'variables')  # 全局变量
        }
        print(datas)
        return Response(datas)
