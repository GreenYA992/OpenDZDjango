from django.urls import path

from .views import EmployeeDetailViews, EmployeeListViews

app_name = "employees"

urlpatterns = [
    path("", EmployeeListViews.as_view(), name="list"),
    path("<int:pk>/", EmployeeDetailViews.as_view(), name="detail"),
]
