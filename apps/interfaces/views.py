import os
from datetime import datetime

from django.conf import settings
from .models import Interfaces
from .serializers import InterfacesModelSerializer,ConfiguresByInterfacesIdModelSerializer,TestcasesByInterfaceIdModelSerializer,InterfaceRunModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework import viewsets
from rest_framework.decorators import action

from utils import common
from envs.models import Envs
from interfaces.models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
import logging
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')
class InterfacesViewSet(viewsets.ModelViewSet):
    """
        list:
        获取接口列表信息

        retrive:
        获取项目详情数据

        create:
        创建接口

        read:
        查看接口详情

        update:
        更新接口信息

        partial_update:
        部分更新接口信息

        delete:
        删除接口

        configs：
        获取接口配置

        testcases:
        获取某个接口下的用例

        run:
        执行接口下的用例
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    pagination_class = MyPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name','tester', 'id']
    ordering_fields = ['id', 'name']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            interface_id = item.get('id')
            #当前接口的用例数
            testcases =Testcases.objects.filter(interface_id=interface_id).count()
            item["testcases"] = testcases
            configures = Configures.objects.filter(interface_id=interface_id).count()
            #当前接口的配置总数
            item["configures"] = configures
        return response


    # @action(detail=True)
    # def project(self,request,*args,**kwargs):
    #     project=self.get_object()
    #     serializer_obj = self.get_serializer(instance=project)
    #     return Response(serializer_obj.data)
    @action(methods=['get'], detail=True)
    def testcases(self, request, *args, **kwargs):
        """
        Returns a list of all the testcases names by interface id
        """
        # testcase_objs = Testcases.objects.filter(interface_id=pk)
        # one_list = []
        # for obj in testcase_objs:
        #     one_list.append({
        #         'id': obj.id,
        #         'name': obj.name
        #     })
        # return Response(data=one_list)

        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['testcases']
        return response

    @action(methods=['get'], detail=True)
    def configs(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['configures']
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()

        # 项目下的所有接口模型对象
        testcase_qs = Testcases.objects.filter(interface=instance)
        # 如果用例模型对象不存在，说明接口下没有用例
        if not testcase_qs.exists():
            data = {
                'ret': False,
                'msg': '此接口下无用例，无法运行'
            }
            return Response(data, status=400)

        # 需要执行的所有用例模型对象的的列表
        runnable_testcase_obj = list(testcase_qs)

        if len(runnable_testcase_obj) == 0:
            data = {
                'ret': False,
                'msg': '此接口下无用例，无法运行'
            }
            return Response(data, status=400)

        # 遍历 用例模型对象的的列表，生成yaml用例文件
        for testcase_obj in runnable_testcase_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 运行此次执行生成的时间戳目录下的所有的用例yaml文件并生成报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == "testcases":
            return TestcasesByInterfaceIdModelSerializer
        elif self.action == 'configs':
            return ConfiguresByInterfacesIdModelSerializer
        elif self.action == 'run':
            return InterfaceRunModelSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        if self.action == 'run':
            pass
        else:
            serializer.save()