from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.trek_list,
        name="trek_list"
    ),

    path(
        "add/",
        views.add_trek,
        name="add_trek"
    ),

    path(
        "edit/<int:pk>/",
        views.edit_trek,
        name="edit_trek"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_trek,
        name="delete_trek"
    ),

]