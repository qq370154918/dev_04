import json
import os
from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from django.conf import settings

import logging
from utils import common,handle_datas
from .models import Testcases
from envs.models import Envs
from interfaces.models import Interfaces
from .serializers import TestcasesModelSerializer,TestcasesRunModelSerializer
from .utils import handel_request_data,handel_test_data, handel_test_data_validate, handel_test_data_variables, handel_test_data_hooks

# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')

class TestcasesViewSet(viewsets.ModelViewSet):
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
    queryset = Testcases.objects.all()
    serializer_class = TestcasesModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    '''
    def retrieve(self, request, *args, **kwargs):
        # 获取当前用例的模型类对象
        testcase_obj = self.get_object()
        # 获取用例所属项目id
        selected_project_id = Interfaces.objects.get(id=testcase_obj.interface_id).project_id

        # 获取include内数据
        include = json.loads(testcase_obj.include,encoding='utf-8')
        selected_configure_id = include.get('config')
        selected_testcase_id = include.get('testcases')

        # 获取数据库request字段内容(test下)
        test_data = json.loads(testcase_obj.request,encoding='utf-8').get('test')
        print(test_data)
        test_request_data = test_data.get('request')

        method = test_request_data.get('method')
        url = test_request_data.get('url')
        # 参数格式 json、data、param
        if 'json' in test_request_data.keys():
            # jsonVariable = json.dumps(test_request_data.get('json'))
            jsonVariable = str(test_request_data.get('json'))

        else:
            jsonVariable = 'null'

        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": testcase_obj.interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": method,
            "url": url,
            "param": handel_request_data(test_request_data, 'params'),
            "header": handel_request_data(test_request_data, 'headers'),
            "variable": handel_request_data(test_request_data, 'data'),  # form表单请求数据
            "jsonVariable": jsonVariable,
            "extract": handel_test_data(test_data, 'extract'),
            "validate": handel_test_data_validate(test_data, 'validate'),
            "globalVar": handel_test_data_variables(test_data, 'variables'),  # 变量
            "parameterized": handel_test_data(test_data, 'parameters'),
            "setupHooks": handel_test_data_hooks(test_data, 'setupHooks'),
            "teardownHooks": handel_test_data_hooks(test_data, 'teardownHooks'),
        }
        print(datas)
        return Response(datas)
    '''
    def retrieve(self, request, *args, **kwargs):
        """获取用例详情信息"""
        # Testcase对象
        testcase_obj = self.get_object()

        # 用例前置信息
        # testcase_include = eval(testcase_obj.include)
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')

        # 用例请求信息
        # testcase_request = eval(testcase_obj.request)
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        testcase_request_datas = testcase_request.get('test').get('request')

        # 处理用例的validate列表
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为[{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_datas.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json数据
        # testcase_json_datas = str(testcase_request_datas.get('json'))
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data3(testcase_extract_datas)

        # 处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')

        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": testcase_request_datas.get('method'),
            "url": testcase_request_datas.get('url'),
            "param": testcase_params_list,
            "header": testcase_headers_list,
            "variable": testcase_form_datas_list,   # form表单请求数据
            "jsonVariable": testcase_json_datas,

            "extract": testcase_extract_datas_list,
            "validate": testcase_validate_list,
            "globalVar": testcase_variables_list,   # 变量
            "parameterized": testcase_parameters_datas_list,
            "setupHooks": testcase_setup_hooks_datas_list,
            "teardownHooks": testcase_teardown_hooks_datas_list,
        }
        return Response(datas)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 获取testcase对象
        instance=self.get_object()
        response=super().create(request, *args, **kwargs)
        env_id=response.data.serializer.validated_data.get('env_id')

        # 构造一个以时间戳命名的文件路径
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建目录
        os.mkdir(testcase_dir_path)

        env = Envs.objects.filter(id=env_id).first()
        # 生成yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)

        # 运行用例（生成报告）
        return common.run_testcase(instance, testcase_dir_path)

    '''
    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['interfaces']
        return Response(response.data)
    '''
    def get_serializer_class(self):
        return TestcasesRunModelSerializer if self.action == 'run' else self.serializer_class

    def perform_create(self,serializer):
        # 重写父类的perform_create方法，如果action为run，则不调用save(仅为了调用父类的create方法进行入参校验)
        if self.action == 'run':
            pass
        else:
            serializer.save()
