# -*- coding: utf-8 -*-
import os
import locale
import platform
import json
from datetime import datetime

from rest_framework.response import Response
import yaml
from httprunner import HttpRunner

from reports.models import Reports
from configures.models import Configures
from testcases.models import Testcases
from debugtalks.models import DebugTalks

def datetime_fmt():
    # 判断当前运行系统
    print(platform.system())
    if platform.system().lower().count('windows')>0:
        locale.setlocale(locale.LC_CTYPE, "Chinese")
    return '%Y年%m月%d日 %H:%M:%S'

def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def generate_testcase_file(instance, env, testcase_dir_path):
    '''生成执行用例的yaml配置文件'''
    testcase_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 获取include信息
    include = json.loads(instance.include, encoding='utf-8')

    #如果config存在于include 且不为null
    if 'config' in include and include.get('config'):
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        # 如果数据库有此条config数据。组装config
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            # 将base_url添加至指定位置
            config_request['config']['request']['base_url'] = env.base_url if env else ''
            # 用新的config配置取代自定义的config配置
            testcase_list[0] = config_request

    # 如果testcase存在于include且前置用例不为空，组装前置用例
    if 'testcases' in include and include.get('testcases'):
        for testcase_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            testcase_list.append(testcase_request)

    # 获取request字段(当前用例)
    request = json.loads(instance.request, encoding='utf-8')
    testcase_list.append(request)

    # 获取用例所属接口名称
    interface_name = instance.interface.name
    project_name=instance.interface.project.name

    # 项目目录
    project_dir_path = os.path.join(testcase_dir_path, project_name)
    # 用例目录
    testcase_dir_path=os.path.join(project_dir_path,interface_name)

    # 如果项目目录不存在。创建项目目录
    if not os.path.exists(project_dir_path):
        os.makedirs(project_dir_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(project_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)
    # 如果用例目录不存在，创建用例目录
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    #创建yaml文件并写入
    with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), "w", encoding="utf-8") as f:
        yaml.dump(testcase_list, f, allow_unicode=True)


def run_testcase(instance, testcase_dir_path):

    # 1、运行用例
    runner = HttpRunner()
    try:
        runner.run(testcase_dir_path)
    except:
        res = {'ret': False, 'msg': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(runner, instance.name)

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
    }
    return Response(data, status=201)


if __name__ == '__main__':
    print(datetime_fmt())