# models.py
from user_app.models import BUser
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)
    booster = models.ForeignKey(BUser, related_name='boosting_rooms', on_delete=models.CASCADE)
    player = models.ForeignKey(BUser, related_name='playing_rooms', on_delete=models.CASCADE)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(BUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
