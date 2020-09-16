# -*- coding: utf-8 -*-

# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('summary/', views.SummaryView.as_view()),
# ]

from django.urls import path
from rest_framework.routers import DefaultRouter
from summary.views import SummaryView

router = DefaultRouter()

urlpatterns = [
    path('summary/', SummaryView.as_view()),
]

urlpatterns += router.urls