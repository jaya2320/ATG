from django.urls import re_path

from .consumers import  ChatRoomConsumer

websocket_urlpatterns = [
     re_path(r'^ws/(?P<room_name>[^/]+)/', ChatRoomConsumer.as_asgi()),
  ]