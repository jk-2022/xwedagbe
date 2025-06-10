from django.urls import path, re_path
from .consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat-notifications/$", NotificationConsumer.as_asgi()),
]
