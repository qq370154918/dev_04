
from django.urls import path
from .views import DebugTalksViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register(r"debugtalks", DebugTalksViewSet)

urlpatterns = []

urlpatterns += router.urls
