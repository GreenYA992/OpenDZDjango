from django.urls import path

from . import views
from .views import EmployeeDetailViews, EmployeeListViews

app_name = "employees"

urlpatterns = [
    path("", EmployeeListViews.as_view(), name="list"),
    path("<int:pk>/", EmployeeDetailViews.as_view(), name="detail"),
    path("<int:pk>/add-image/", views.add_employee_image, name="add_image"),
    path("<int:pk>/set-main-photo/", views.set_main_photo, name="set_main_photo"),
    path("<int:pk>/delete-image/", views.delete_employee_image, name="delete_image"),
]
