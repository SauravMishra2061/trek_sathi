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
    path(
    "enquiry/<int:package_id>/",
    views.start_enquiry,
    name="start_enquiry",
    ),
    path(
    "my-conversations/",
    views.my_conversations,
    name="my_conversations",
    ),

]