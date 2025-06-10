from rest_framework import serializers
from .models import Room, Message
# from django.contrib.auth import get_user_model

class MessageSerializer(serializers.ModelSerializer):
    sender_phone = serializers.CharField(source="sender.phone_number", read_only=True)
    recipient_phone = serializers.CharField(source="receiver.phone_number", read_only=True)

    class Meta:
        model = Message
        fields = ["id","room","sender","receiver", "sender_phone", "recipient_phone","content","timestamp","is_read",]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


