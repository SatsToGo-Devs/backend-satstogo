"""
ASGI config for sattogo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

from api import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sattogo.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
            re_path(r"ws/notifications/(?P<k1>\w+)/$", consumers.WebSocketConsumer.as_asgi()),
        ]
        ),
        )
    )
})