from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_choice, name="login_choice"),
    path("register/", views.register_choice, name="register_choice"),
    path("register/trekker/", views.trekker_register, name="trekker_register"),
    path("register/company/", views.company_register, name="company_register"),
]
