
from django.urls import path
from .views import InterfacesViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register(r"interfaces", InterfacesViewSet)

urlpatterns = [
    # path('interfaces/<int:pk>/',InterfacesViewSet.as_view(
    #     {
    #         'get': 'retrieve',
    #         'put': 'update',
    #         'patch':'partial_update',
    #         'delete': 'destroy'
    #     }
    # )),
    # path('interfaces/',InterfacesViewSet.as_view(
    #     {
    #         'get': 'list',
    #         'post': 'create'
    #     }
    # ))
]

urlpatterns += router.urls
