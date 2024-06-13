# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Room, Message

"""
    Warning

    If you enable this option and there is concurrent access to the async-unsafe parts of Django,
    you may suffer data loss or corruption. Be very careful and do not use this in production environments.
    
    we enable this if we want to retrieve messages ( or any non-async ORM operations ) in an async env 
"""
import os
import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# django.setup()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        print(f"User {self.user} is trying to connect to room {self.room_name}")
        # Check if user has access to the room
        if not await self.user_has_access():
            print('user has no access')
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"User {self.user} added to group {self.room_group_name}")

        # Load previous messages
        # messages = await self.get_messages()
        # for message in messages:
        #     await self.send(text_data=json.dumps({"message": message.content, "user": message.user.username}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print(f"Received message: {message} from user: {self.user}")

        # Save message to database
        new_message = await self.save_message(message)

        print(f"New message saved: {new_message.content}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": new_message.content,
                "user": self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        print(f"Broadcasting message: {message} from user: {user}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user
        }))

    @database_sync_to_async
    def user_has_access(self):
        try:
            room = Room.objects.get(name=self.room_name)
            res = room.booster == self.user or room.player == self.user or self.user.is_superuser or self.user.is_staff
            return res
        except Exception as e:
            return False

    # async def get_messages(self):
    #     room = await self.get_room()
    #     messages = await self.get_messages_objects(room.id)
    #     return messages
    #
    # @sync_to_async
    # def get_room(self):
    #     return Room.objects.get(name=self.room_name)
    #
    # @sync_to_async
    # def get_messages_objects(self,room_id):
    #     print('OBJ ',Message.objects.filter(room=room_id))
    #     return Message.objects.filter(room=room_id)

    @database_sync_to_async
    def save_message(self, content):
        print('save message')
        room = Room.objects.get(name=self.room_name)
        return Message.objects.create(room=room, user=self.user, content=content)
