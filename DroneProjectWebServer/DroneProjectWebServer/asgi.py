"""
ASGI config for DroneProjectWebServer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from DroneProjectWebServer.DroneProjectWebServer import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DroneProjectWebServer.settings')

#application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/gps/", consumers.GPSConsumer.as_asgi()),
            ]
        )
    ),
})
