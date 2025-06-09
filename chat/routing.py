from django.urls import path, re_path
from .consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    # path('ws/chat/<int:room_id>/', ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]
