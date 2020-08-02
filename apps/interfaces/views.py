from django.http import JsonResponse

from .models import Interfaces
from .serializers import InterfacesModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=True)
    def project(self,request,*args,**kwargs):
        project=self.get_object()
        serializer_obj = self.get_serializer(instance=project)
        return Response(serializer_obj.data)

    # def get_serializer_class(self):
    #     if self.action == 'project':
    #         return ProjectsByInterfacesModelSerializer
    #     else:
    #         return self.serializer_class