
from django.urls import path
from .views import ConfiguresViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register(r"configures", ConfiguresViewSet)

urlpatterns = []

urlpatterns += router.urls
