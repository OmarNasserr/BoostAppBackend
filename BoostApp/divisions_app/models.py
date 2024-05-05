import os.path
from datetime import datetime
from django.db import models
from games_app.models import Game

# Create your models here.


class Division(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, )
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='divisions')
    created_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)
    updated_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)

    def __str__(self):
        return self.name



def divisions_icons_location(instance, filename):
    upload_path = f'media/game_images/{instance.division.game_id.name}/divisions_icons/{instance.division.name}'
    return os.path.join(upload_path,filename)

class DivisionImage(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division_icon')
    image = models.ImageField(upload_to=divisions_icons_location, blank=True, null=True, )

    def __str__(self):
        return self.division.name