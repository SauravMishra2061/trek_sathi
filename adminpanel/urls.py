from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("regions/", views.admin_regions, name="admin_regions"),
    path("treks/", views.admin_treks, name="admin_treks"),
    path("companies/", views.admin_companies, name="admin_companies"),
    path("users/", views.admin_users, name="admin_users"),
    path("trek-requests/",views.trek_requests,name="admin_trek_requests"),
    path("trek-requests/<int:pk>/",views.review_trek_request,name="review_trek_request"),
]