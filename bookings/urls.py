from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.company_bookings,
        name="company_bookings",
    ),
    path(
    "<int:pk>/",
    views.booking_detail,
    name="booking_detail",
    ),
]