from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from chat.serializers import MessageSerializer
from .models import Room, Message
from django.shortcuts import get_object_or_404
from users.models import CustomUser 

class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        user = request.user
        room = get_object_or_404(Room, id=room_id)

        # Vérifier que l'utilisateur fait bien partie de la room
        if user != room.user1 and user != room.user2:
            return Response({"detail": "Vous n'avez pas accès à cette room."}, status=403)

        # Récupérer tous les messages de la room
        messages = Message.objects.filter(room=room).order_by("timestamp")

        # Marquer comme lus les messages reçus et non lus
        unread_messages = messages.filter(receiver=user, is_read=False)
        unread_messages.update(is_read=True)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class UserRoomsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Trouver les rooms où l'utilisateur est impliqué
        rooms = Room.objects.filter(user1=user) | Room.objects.filter(user2=user)
        data = []

        for room in rooms:
            last_message = Message.objects.filter(room=room).order_by("-timestamp").first()
            other_user = room.user1 if room.user2 == user else room.user2

            unread_count = Message.objects.filter(
                room=room,
                receiver=user,
                is_read=False
            ).count()

            data.append({
                "room_id": room.id,
                "other_user": {
                    "id": other_user.id,
                    "phone_number": other_user.phone_number,
                    "full_name": other_user.full_name
                },
                "unread_messages": unread_count,
                "last_message": {
                    "sender_id": last_message.sender.id if last_message else None,
                    "sender_phone": last_message.sender.phone_number if last_message else None,
                    "content": last_message.content if last_message else None,
                    "timestamp": last_message.timestamp.isoformat() if last_message else None
                } if last_message else None
            })

        return Response(data)

class GetOrCreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("other_user_id")
        user = request.user
        if not other_user_id or int(other_user_id) == user.id:
            return Response({"error": "Invalid user ID"}, status=400)

        try:
            room = Room.objects.filter(
                (Q(user1_id=user.id) & Q(user2_id=other_user_id)) |
                (Q(user1_id=other_user_id) & Q(user2_id=user.id))
            ).first()
            if not room:
                other_user = get_object_or_404(CustomUser, id=other_user_id)
                room = Room.objects.create(user1=user, user2=other_user)

            return Response({"room_id": room.id})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

