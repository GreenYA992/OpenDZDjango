from django.urls import path, include
# noinspection PyUnresolvedReferences
from rest_framework.routers import DefaultRouter
from .api_views import WorkplaceViewSet

router = DefaultRouter()
router.register(r'workplaces', WorkplaceViewSet, basename='workplace-api')

urlpatterns = [
    path('', include(router.urls)),
]