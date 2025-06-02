import asyncio
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from jwt import decode as jwt_decode
from django.conf import settings

from notifications.models import Notification
from users.models import CustomUser

class AdminNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user()

        if self.user and self.user.is_authenticated:
            # Groupe pour les notifications admin
            if self.user.is_staff:
                await self.channel_layer.group_add("admin_notifications", self.channel_name)
                print(f"Admin connecté à admin_notifications")
            # Groupe personnel pour l'utilisateur
            await self.channel_layer.group_add(f"user_{self.user.id}", self.channel_name)
            print(f"Utilisateur connecté à user_{self.user.id}")
            await self.accept()
        else:
            await self.close()

         # Envoie les notifications non lues à la connexion
        unread = await self.get_unread_notifications()
        for notif in unread:
            await self.send(text_data=json.dumps({
                "type": notif.type,
                "message": notif.message,
                "id": notif.id
            }))

    

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(f"user_{self.user.id}", self.channel_name)
            if self.user.is_staff:
                await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    @database_sync_to_async
    def get_unread_notifications(self):
        # return Product.objects.all()
        return list(Notification.objects.filter(recipient=self.user, is_read=False))

    async def receive_json(self, content):
        print("Message reçu du client :", content)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "mark_read":
            notif_id = data.get("id")
            await self.mark_notification_read(notif_id)

    @database_sync_to_async
    def mark_notification_read(self, notif_id):
        Notification.objects.filter(id=notif_id, recipient=self.user).update(is_read=True)

    async def demande_notification(self, event):
        message = event["message"]
        type=event["type"]
        await self.send(text_data=json.dumps({"message": message,"type": type}))

    async def promotion_notification(self, event):
        message = event["message"]
        await self.send_json({
            "type": "promotion_notification",
            "message": message
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

