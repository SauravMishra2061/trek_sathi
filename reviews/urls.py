from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.company_reviews,
        name="company_reviews",
    ),

]