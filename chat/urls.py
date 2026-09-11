from django.urls import path

from .views import chat_page, heartbeat, online_users


urlpatterns = [
    path("", chat_page, name="chat"),
    path("heartbeat/", heartbeat, name="heartbeat"),
    path("online-users/", online_users, name="online_users"),
]