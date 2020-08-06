
from .serializers import EnvsModelSerializer,EnvsNameModelSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework import viewsets
from rest_framework.decorators import action

from envs.models import Envs
import logging
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')
class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    pagination_class = MyPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['id']

    @action(detail=False)
    def names(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNameModelSerializer
        else:
            return self.serializer_class