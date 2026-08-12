from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.company_reviews,
        name="company_reviews",
    ),

    path(
        "create/<int:booking_id>/",
        views.create_review,
        name="create_review",
    ),

]