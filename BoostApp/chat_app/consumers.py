# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # Check if user has access to the room
        if not await self.user_has_access():
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load previous messages
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({"message": message.content, "user": message.user.username}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Save message to database
        new_message = await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": new_message.content, "user": self.user.username}
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user": user}))

    @database_sync_to_async
    def user_has_access(self):
        try:
            room = Room.objects.get(name=self.room_name)
            return room.booster == self.user or room.player == self.user or self.user.is_superuser or self.user.is_staff
        except Room.DoesNotExist:
            return False

    @database_sync_to_async
    def get_messages(self):
        room = Room.objects.get(name=self.room_name)
        return Message.objects.filter(room=room)

    @database_sync_to_async
    def save_message(self, content):
        room = Room.objects.get(name=self.room_name)
        return Message.objects.create(room=room, user=self.user, content=content)
