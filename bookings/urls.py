from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.company_bookings,
        name="company_bookings",
    ),

    path(
        "create/<int:package_id>/",
        views.create_booking,
        name="book_package",
    ),

    path(
        "<int:pk>/",
        views.booking_detail,
        name="booking_detail",
    ),





    path(
        "<int:pk>/approve/",
        views.approve_booking,
        name="approve_booking",
    ),

    path(
        "<int:pk>/reject/",
        views.reject_booking,
        name="reject_booking",
    ),

    path(
        "<int:pk>/complete/",
        views.complete_booking,
        name="complete_booking",
    ),
    
]