from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatapp.consumers import ChatRoomConsumer,PersonalChatConsumer,GroupChatRoomConsumer
from channels.auth import AuthMiddlewareStack
application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter([
        path('ws/<str:room_name>/',ChatRoomConsumer.as_asgi()),
        path('ws/joingroup/<str:room_name>/',GroupChatRoomConsumer.as_asgi()),
        path('ws/personal/<str:username>/',PersonalChatConsumer.as_asgi()),
    ])
    )
})