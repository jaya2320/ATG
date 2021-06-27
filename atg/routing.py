from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatapp.consumers import ChatRoomConsumer,PersonalChatConsumer
from channels.auth import AuthMiddlewareStack
application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter([
        path('ws/<str:room_name>/',ChatRoomConsumer.as_asgi()),
        path('ws/personal/<str:username>/',PersonalChatConsumer.as_asgi()),
    ])
    )
})