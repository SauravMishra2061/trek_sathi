from django.urls import path
from . import views

urlpatterns = [
    path("trekker/", views.trekker_dashboard, name="trekker_dashboard"),
]