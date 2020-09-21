import json
import logging
import os
from datetime import datetime
from envs.models import Envs
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
# from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from .models import Projects
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from testcases.models import Testcases
from utils import common

from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, \
    InterfacesByProjectIdModelSerializer, ProjectRunModelSerializer

# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
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
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            # item为一条项目数据所在的字典
            # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
            project_id = item.get('id')
            # interface_count = Interfaces.objects.filter(project_id=project_id).count()
            # interface_qs = Interfaces.objects.filter(project_id=project_id)
            # for obj in interface_qs:
            #     interface_id = obj.id
            #     TestCase.ojbects.filter(interface_id=interface_id).count()

            # a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
            # b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（还需要在外键字段上设置related_name）
            # c.values可以指定需要查询的字段（默认为所用字段）
            # d.可以给聚合函数指定别名，默认为testcases__count
            interfaces_obj = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=project_id)
            #当前项目的接口数
            item["interfaces"]=len(interfaces_obj)
            testcases=0
            for i in interfaces_obj:
                testcases += i['testcases']
            #当前项目的用例总数
            item["testcases"] = testcases
            testsuits =Testsuits.objects.filter(project_id=project_id).count()
            #当前项目的套件总数
            item["testsuits"] = testsuits
            interfaces_configures = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(project_id=project_id)
            configures=0
            for i in interfaces_configures:
                configures += i['configures']
            #当前项目的配置总数
            item["configures"] = configures
        return response


    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['interfaces']
        return Response(response.data)

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
        interface_qs = Interfaces.objects.filter(project=instance)
        # 如果接口模型对象不存在，说明项目下没有接口，也不会有用例
        if not interface_qs.exists():
            data = {
                'ret': False,
                'msg': '此项目下无接口，无法运行'
            }
            return Response(data, status=400)

        # 定义一个需要执行的所有用例模型对象的的列表
        runnable_testcase_obj = []
        for interface_obj in interface_qs:
            # 当前接口项目的用例所在查询集对象
            testcase_qs = Testcases.objects.filter(interface=interface_obj)
            if testcase_qs.exists():
                # 将两个列表合并
                runnable_testcase_obj.extend(list(testcase_qs))

        if len(runnable_testcase_obj) == 0:
            data = {
                'ret': False,
                'msg': '此项目下无用例，无法运行'
            }
            return Response(data, status=400)

        # 遍历 用例模型对象的的列表，生成yaml用例文件
        for testcase_obj in runnable_testcase_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 运行此次执行生成的时间戳目录下的所有的用例yaml文件并生成报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectIdModelSerializer
        elif self.action == 'run':
            return ProjectRunModelSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        if self.action == 'run':
            pass
        else:
            serializer.save()
