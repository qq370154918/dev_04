import json
import logging
import os
from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from django.conf import settings

from utils import common
from .models import Testsuits
from testcases.models import Testcases
from envs.models import Envs
from .serializers import TestsuitsModelSerializer,TestsuitsDetailModelSerializer,TestsuitRunModelSerializer

class TestsuitsViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     data = {
    #         'name': instance.name,
    #         'project_id': instance.project_id,
    #         'include': instance.include
    #     }
    #     return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        # 获取env_id
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()

        # 获取include下的所有接口id
        testsuit_interfaces = eval(instance.include)
        testsuit_testcase=eval(instance.include)
        # 如果include为空，说明套件下没有用例
        if not testsuit_testcase:
            data = {
                'ret': False,
                'msg': '此套件下无用例，无法运行'
            }
            return Response(data, status=400)

        # 定义需要执行的所有用例模型对象的的列表
        runnable_testcase_obj = []
        for interfaces_id in testsuit_interfaces:
            testcase_qs=Testcases.objects.filter(interface_id=interfaces_id)
            if testcase_qs.exists():
                # 将两个列表合并
                runnable_testcase_obj.extend(list(testcase_qs))

        if len(runnable_testcase_obj) == 0:
            data = {
                'ret': False,
                'msg': '此套件下无用例，无法运行'
            }
            return Response(data, status=400)

        # 遍历 用例模型对象的的列表，生成yaml用例文件
        for testcase_obj in runnable_testcase_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 运行此次执行生成的时间戳目录下的所有的用例yaml文件并生成报告
        return common.run_testcase(instance, testcase_dir_path)


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestsuitsDetailModelSerializer
        if self.action == 'run':
            return TestsuitRunModelSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        if self.action == 'run':
            pass
        else:
            serializer.save()
