
from .serializers import DebugTalksModelSerializer
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework import viewsets
from .models import DebugTalks
from rest_framework.decorators import action

import logging
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')
class DebugTalksViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer
    pagination_class = MyPagination

