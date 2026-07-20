from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
    path("packages/", views.company_packages, name="company_packages"),
    path("bookings/", views.company_bookings, name="company_bookings"),
    path("messages/", views.company_messages, name="company_messages"),
    path("earnings/", views.company_earnings, name="company_earnings"),
    path("reviews/", views.company_reviews, name="company_reviews"),
    path("profile/", views.company_profile, name="company_profile"),
    path("", views.company_list, name="company_list"),
    path("<int:pk>/", views.company_detail, name="company_detail"),

    path("<int:pk>/approve/", views.approve_company, name="approve_company"),

    path("<int:pk>/reject/", views.reject_company, name="reject_company"),

    path("<int:pk>/suspend/", views.suspend_company, name="suspend_company"),
    

]