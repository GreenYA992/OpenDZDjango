from django.urls import path

from . import views

app_name = "workplaces"

urlpatterns = [
    path("", views.WorkplaceListViews.as_view(), name="workplaces"),
    path("<int:pk>/", views.workplace_detail, name="workplace_detail"),
    path("<int:pk>/book/", views.WorkplaceBookView.as_view(), name="booking"),
    path("add_workplace/", views.WorkplaceCreateView.as_view(), name="add_workplace"),
    path(
        "<int:pk>/release/",
        views.WorkplaceReleaseView.as_view(),
        name="clear_workplace",
    ),
    path(
        "<int:pk>/delete/", views.WorkplaceDeleteView.as_view(), name="delete_workplace"
    ),
]
