from django.urls import path

from . import views

app_name = "workplaces"

urlpatterns = [

    path('', views.WorkplaceListViews.as_view(), name='workplace-list'),
    path('create/', views.WorkplaceCreateView.as_view(), name='workplace-create'),
    path('<int:pk>/', views.workplace_detail, name='workplace-detail'),
    path('<int:pk>/book/', views.WorkplaceBookView.as_view(), name='workplace-book'),
    path('<int:pk>/release/', views.WorkplaceReleaseView.as_view(), name='workplace-release'),
    path('<int:pk>/delete/', views.WorkplaceDeleteView.as_view(), name='workplace-delete'),

]