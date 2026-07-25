from django.urls import path
from . import views

urlpatterns = [
    path("", views.package_list, name="package_list"),
    path("add/", views.add_package, name="add_package"),

    path("<int:pk>/", views.package_detail, name="package_detail"),
    path("<int:pk>/edit/", views.edit_package, name="edit_package"),
    path("<int:pk>/delete/", views.delete_package, name="delete_package"),
]