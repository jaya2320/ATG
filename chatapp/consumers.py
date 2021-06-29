from channels.consumer import SyncConsumer,AsyncConsumer
from asgiref.sync import async_to_sync,sync_to_async
from django.contrib.auth.models import User
from chatapp.models import Thread,Message,Messagepublic,Profile
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string


class ChatRoomConsumer(AsyncWebsocketConsumer):
    print("in publicchat---------------------------------------------------------")
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = '%s' % self.room_name
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        await self.save_message(username,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass

    @sync_to_async
    def save_message(self,username,message):
        

        Messagepublic.objects.create(user=username,content=message)







class PersonalChatConsumer(AsyncWebsocketConsumer):
    print("in personalchat---------------------------------------------------------")
    async def connect(self):
        me=self.scope['user']
        other_username=self.scope['url_route']['kwargs']['username']
        other_user=await sync_to_async(User.objects.get)(username=other_username)
        self.thread_obj=await sync_to_async(Thread.objects.get_or_create_personal_thread)(me,other_user)
        self.room_name='personal_thread_'+str(self.thread_obj.id)
        
        
        print(me,other_user,self.room_name,self.thread_obj.id,'------------------------------------------------------')
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        user=self.scope['user']
        if user.is_authenticated:
            await self.update_user_status (user, True)
      
        print('group_add------------------------------')
        
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        user = self.scope ['user']
        if user.is_authenticated:
            await self.update_user_status (user, False)
      
    print('disconnected-------------------------------')
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username
        
        await self.save_message(username,message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'websocket.message',
                'message': message,
                'username': username,
            }
        )
    print('recieve------------------------------------')    
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass
    print('chatroom_message--------------------------------')
    @sync_to_async
    def save_message(self,username,message):
        userid=User.objects.get(username=username)
        
        Message.objects.create(thread=self.thread_obj,sender=userid,content=message)
        print('message created---------------------------------------------------')


    @sync_to_async
    def update_user_status (self, user, status):
        return Profile.objects.filter (user_id = user.pk) .update (status = status)

