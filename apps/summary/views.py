import logging
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuits.models import Testsuits
from configures.models import Configures
from envs.models import Envs
from debugtalks.models import DebugTalks
from reports.models import Reports

logger = logging.getLogger('mytest')

class SummaryView(APIView):
    """
    get:
    获取统计信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 获取当前登录的用户名
        username = request.user.username

        # 当前登录的用户模型类对象
        current_user_obj = User.objects.get(username=username)
        role = '管理员' if current_user_obj.is_superuser else '普通用户'
        date_joined = datetime.strftime(current_user_obj.date_joined, '%Y-%m-%d %H:%M:%S')
        last_login = datetime.strftime(current_user_obj.last_login,
                                       '%Y-%m-%d %H:%M:%S') if current_user_obj.last_login else ""
        # 获取项目总数
        projects_count = Projects.objects.all().count()
        # 获取接口总数
        interfaces_count = Interfaces.objects.all().count()
        # 获取用例总数
        testcases_count = Testcases.objects.all().count()
        # 获取套件总数
        testsuits_count = Testsuits.objects.all().count()
        # 获取配置总数
        configures_count = Configures.objects.all().count()
        # 获取环境变量总数
        envs_count = Envs.objects.all().count()
        # 获取内置函数总数
        debug_talks_count = DebugTalks.objects.all().count()
        # 获取报告总数
        reports_ps = Reports.objects.all()
        reports_count = reports_ps.count()

        total_res = sum([obj.count for obj in reports_ps])
        success_res = sum([obj.success for obj in reports_ps])

        try:
            # 成功率
            success_rate = round((success_res / total_res), 2) * 100
            # 失败率
            fail_rate = 100 - success_rate
        except ZeroDivisionError:
            success_rate = 0
            fail_rate = 0
        response = {
            'user': {
                'username': username,
                'role': role,
                'date_joined': date_joined,
                'last_login': last_login
            },
            'statistics': {
                'projects_count': projects_count,
                'interfaces_count': interfaces_count,
                'testcases_count': testcases_count,
                'testsuits_count': testsuits_count,
                'configures_count': configures_count,
                'envs_count': envs_count,
                'debug_talks_count': debug_talks_count,
                'reports_count': reports_count,
                'success_rate': success_rate,
                'fail_rate': fail_rate
            }
        }

        return Response(response, status=status.HTTP_200_OK)


