# -*- coding: utf-8 -*-

from django.urls import path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

# from projects.views import
from . import views


# 定义路由对象
# router = SimpleRouter()
# DefaultRouter相比SimpleRouter，自动添加了一条根路径的路由 /  -> 可浏览器的api页面
router = DefaultRouter()
# 使用路由对象.register()方法，来进行注册
# a.第一个参数指定路由前缀，r'子应用名小写'
# b.第二个参数指定视图集类即可，不要调用.as_view()
router.register(r'testcases', views.TestcasesViewSet)

urlpatterns = [
]
urlpatterns += router.urls

