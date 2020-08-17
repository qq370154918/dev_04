# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views


urlpatterns = [
    path('summary/', views.SummaryViewSet.as_view()),
]
