from django.db import models
# from django.contrib.auth import get_user_model
from django.conf import settings

from users.models import CustomUser

class Room(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='room_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
    
    def get_receiver(self, sender):
        return self.user2 if self.user1 == sender else self.user1

    def __str__(self):
        return f"Room {self.user1.phone_number} - {self.user2.phone_number}"

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.phone_number} in room {self.room.id}"
