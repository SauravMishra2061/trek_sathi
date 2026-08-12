from django.urls import path
from . import views

urlpatterns = [
    path("", views.region_list, name="region_list"),
    path("add/", views.add_region, name="add_region"),
    path("edit/<int:pk>/", views.edit_region, name="edit_region"),
    path("delete/<int:pk>/", views.delete_region, name="delete_region"),
    path("<int:pk>/", views.region_detail, name="region_detail"),
]