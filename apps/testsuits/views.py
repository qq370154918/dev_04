import json
import logging

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
# from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from .models import Testsuits
from .serializers import TestsuitsModelSerializer,TestsuitsDetailModelSerializer

class TestsuitsViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     data = {
    #         'name': instance.name,
    #         'project_id': instance.project_id,
    #         'include': instance.include
    #     }
    #     return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestsuitsDetailModelSerializer
        else:
            return self.serializer_class