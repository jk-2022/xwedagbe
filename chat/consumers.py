import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.conf import settings
from jwt import decode as jwt_decode
from django.contrib.auth.models import AnonymousUser
# from jwt_auth.utils import get_user_from_token

from users.models import CustomUser


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user()
        if self.user is None:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}_rooms"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_unread_message(self, event):
        # Reçoit une notif d'un nouveau message non lu
        await self.send_json({
            "type": "notification",
            "room_id": event["room_id"],
            "message_count": event["message_count"],
            "last_message": event["last_message"],
            "timestamp": event["timestamp"],
        })

    @database_sync_to_async
    def get_user(self):
        try:
            # Récupération du token à partir de l'en-tête QueryString
            token = self.scope['query_string'].decode().split('=')[-1]
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data["user_id"]
            return CustomUser.objects.get(id=user_id)
        except Exception as e:
            print("Erreur d'authentification WebSocket :", e)
            return AnonymousUser()



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        self.user = await self.get_user()

        if self.user is None:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        room = await database_sync_to_async(Room.objects.get)(id=self.room_id)
        receiver = await database_sync_to_async(room.get_receiver)(self.user)

        msg=await self.save_message(room, self.user ,receiver, message)
        
        message_count = await database_sync_to_async(lambda: Message.objects.filter(room=room, receiver=receiver, is_read=False).count())()

        await self.channel_layer.group_send(
            f"user_{receiver.id}_rooms",
            {
                "type": "new_unread_message",
                "room_id": room.id,
                "message_count": message_count,
                "last_message":msg.content,
                "timestamp":msg.timestamp.isoformat()
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.id,
                'receiver': receiver.id,
                'sender_phone': self.user.phone_number
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, room, sender, receiver, content):
        return Message.objects.create(room=room, sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_user(self):
        try:
            # Récupération du token à partir de l'en-tête QueryString
            token = self.scope['query_string'].decode().split('=')[-1]
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data["user_id"]
            return CustomUser.objects.get(id=user_id)
        except Exception as e:
            print("Erreur d'authentification WebSocket :", e)
            return AnonymousUser()
