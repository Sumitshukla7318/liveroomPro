# from channels.consumer import AsyncConsumer
from . import consumers
from django.urls import path

websocket_urlpatterns = [
    # path('aws/', consumers.MyJsonWebsocketConsumer.as_asgi()),
    path('aws/', consumers.MySyncConsumer.as_asgi()),
]