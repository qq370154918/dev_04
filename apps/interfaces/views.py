from django.http import JsonResponse

from .models import Interfaces
from .serializers import InterfacesModelSerializer,InterfacesByConfigureIdModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework import viewsets
from rest_framework.decorators import action

from interfaces.models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
import logging
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')
class InterfacesViewSet(viewsets.ModelViewSet):
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

    @action(detail=True)
    def configs(self,request,*args,**kwargs):
        interface_obj=self.get_object()
        serializer_obj = self.get_serializer(instance=interface_obj)
        return Response(serializer_obj.data)

    def get_serializer_class(self):
        if self.action == 'project':
            return InterfacesByConfigureIdModelSerializer
        else:
            return self.serializer_class