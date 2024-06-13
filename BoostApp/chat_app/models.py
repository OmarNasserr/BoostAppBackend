# models.py
from user_app.models import BUser
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)
    booster = models.ForeignKey(BUser, related_name='boosting_rooms', on_delete=models.CASCADE)
    player = models.ForeignKey(BUser, related_name='playing_rooms', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(BUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"message in {self.room.name} from user {self.user.username}"

    class Meta:
        ordering = ('timestamp',)
