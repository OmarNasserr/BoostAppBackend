import os.path
from datetime import datetime
from django.db import models

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, )
    story = models.TextField(blank=True, null=True, )
    most_popular = models.BooleanField(default=False)
    # devisions =
    created_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)
    updated_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)

    def __str__(self):
        return self.name



def game_images_location(instance, filename):
    upload_path = f'media/game_images/{instance.game.name}'
    return os.path.join(upload_path,filename)

class GameImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='pics_from_the_game')
    image = models.ImageField(upload_to=game_images_location, blank=True, null=True, )

    thumbnail = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.game.name