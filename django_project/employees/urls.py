from django.urls import path

from .views import detail, index
from .views import EmployeeListViews, EmployeeDetailViews

app_name = 'employees'

"""
urlpatterns = [
    path("", index),
    path('<int:pk>/', detail),
]
"""
urlpatterns = [
    path("", EmployeeListViews.as_view(), name='list'),
    path('<int:pk>/', EmployeeDetailViews.as_view(), name='detail'),
]
