from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_choice, name="login_choice"),
    path("register/", views.register_choice, name="register_choice"),
    path("register/trekker/", views.trekker_register, name="trekker_register"),
    path("register/company/", views.company_register, name="company_register"),
    path("login/trekker/", views.trekker_login, name="trekker_login"),
    path("login/company/",views.company_login,name="company_login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/",views.profile,name="profile"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("saved-packages/",views.saved_packages,name="saved_packages",),
]
