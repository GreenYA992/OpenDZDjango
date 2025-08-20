from django.urls import path

from .views import EmployeeDetailViews, EmployeeListViews
from . import views

app_name = "employees"

urlpatterns = [
    path("", EmployeeListViews.as_view(), name="list"),
    path("<int:pk>/", EmployeeDetailViews.as_view(), name="detail"),

    path('<int:pk>/add-image/', views.add_employee_image, name='add_image'),
    path('<int:pk>/set-main-photo/', views.set_main_photo, name='set_main_photo'),
    path('<int:pk>/delete-image/', views.delete_employee_image, name='delete_image'),
]
