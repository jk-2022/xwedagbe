"""
ASGI config for habitalink project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""


# myproject/asgi.py
import os
import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import notifications.routing 
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habitalink.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(notifications.routing.websocket_urlpatterns + chat.routing.websocket_urlpatterns)
    ),
})

