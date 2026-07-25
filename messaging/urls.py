from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.company_inbox,
        name="company_messages",
    ),

    path(
        "<int:pk>/",
        views.conversation_detail,
        name="conversation_detail",
    ),

]