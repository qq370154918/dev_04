
from django.urls import path
from .views import EnvsViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register(r"envs", EnvsViewSet)

urlpatterns = []

urlpatterns += router.urls
