# -*- coding: utf-8 -*-

import locale
import platform
import json
import os
from ruamel import yaml

def datetime_fmt():
    # 判断当前运行系统
    if platform. system().lower().count('windows')>0:
        locale.setlocale(locale.LC_CTYPE, "Chinese")
    return '%Y年%m月%d日 %H:%M:%S'


def generate_testcase_file(instance, env, testcase_dir_path):
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
    #组装config
    if include['confing']:
        pass
    #组装前置用例
    if include['testcases']:
        pass
    # 获取request字段
    request = json.loads(instance.request, encoding='utf-8')
    # 获取用例所属接口名称
    interface_name = instance.interface.name
    project_name=instance.interface.project
    path=os.makedirs(f'{testcase_dir_path}/{project_name}/{interface_name}')
    full_path=os.path.join(testcase_dir_path, )
    with open(testcase_dir_path, "w", encoding="utf-8") as f:
        yaml.dump(testcase_list, f, Dumper=yaml.RoundTripDumper)
    pass
