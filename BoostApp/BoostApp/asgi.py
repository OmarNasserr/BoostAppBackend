"""
ASGI config for BoostApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BoostApp.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

"""

    routes different protocols to their respective handlers. In this case, it routes HTTP requests ("http") and
    WebSocket connections ("websocket").
    For HTTP requests, it uses get_asgi_application() to get the standard Django ASGI application.
    For WebSocket connections, it applies authentication middleware (AuthMiddlewareStack) and routes WebSocket URLs to
    appropriate consumers using URLRouter. The websocket_urlpatterns should be defined in your Django app's routing.py
 
"""

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})
