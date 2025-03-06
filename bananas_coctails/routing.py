from django.urls import path
from . import consumers  # Asegúrate de tener un consumer implementado

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]
