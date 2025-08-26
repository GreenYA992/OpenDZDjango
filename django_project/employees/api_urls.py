from django.urls import path, include
# noinspection PyUnresolvedReferences
from rest_framework.routers import DefaultRouter
# noinspection PyUnresolvedReferences
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee-api')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # /api/employees/
]