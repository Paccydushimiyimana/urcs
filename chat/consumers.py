import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat_room, Message
from account.models import MyUser

class ChatConsumerA(AsyncWebsocketConsumer):
      async def connect(self):
            # print(self.scope['url_route']['kwargs']['room'])
            self.user = self.scope['user']
            self.room_name = self.scope['url_route']['kwargs']['room']
            self.room_group_name = 'chat_%s' % self.room_name
            print(self.room_group_name)
            # print(self.room_group_name)           
             # Join room group
            await self.channel_layer.group_add(
                  self.room_group_name,
                  self.channel_name
            )

            await self.accept()

      async def receive(self,text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = text_data_json['sender']
            # print(self)
            # call fx to save message to db
            await self.create_message(message,sender)
            
            # Send message to room group  
            await self.channel_layer.group_send(
                  self.room_group_name,
                  {'type':'chat_message','message': message,'sender':sender}
            )
    
      async def chat_message(self,event):
            # print(event)
            message = event['message']
            sender = event['sender']
            # # Send message to WebSocket
            await self.send(text_data=json.dumps({
                  'room': self.room_name,
                  'message': message,
                  'sender':sender
            }))      
            
      async def disconnect(self, close_code):
            # Leave room group
            await self.channel_layer.group_discard(
                  self.room_group_name,
                  self.channel_name
            )

      @database_sync_to_async
      def create_message(self,message,sender):
            room = Chat_room.objects.get(id=self.room_name)
            sender = MyUser.objects.get(username=sender)
            return Message.objects.create(room=room, sender=sender, content=message)

class ChatConsumerB(AsyncWebsocketConsumer):
      async def connect(self):
            await self.accept()
            await self.channel_layer.group_add('gossip',self.channel_name)
            # print(f' Added to gossip')
                      
      async def disconnect(self,close_code):
            await self.channel_layer.group_discard('gossip',self.channel_name)
            # print(f' Removed from gossip')

      async def user_gossip(self, event):
            data = json.dumps(event)
            await self.send(data)
            # print(f' Got message on gossip')
