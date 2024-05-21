import os.path
from datetime import datetime
from django.db import models
from games_app.models import Game


class Division(models.Model):
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='divisions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, )
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='divisions')
    previous_division = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(default=1.0, decimal_places=2, max_digits=9)
    rank = models.IntegerField(blank=False, null=False)
    created_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)
    updated_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)

    def __str__(self):
        return self.name


def divisions_icons_location(instance, filename):
    upload_path = f'media/game_images/{instance.division.game_id.name}/divisions_icons/{instance.division.name}'
    return os.path.join(upload_path, filename)


class DivisionImage(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division_icon')
    image = models.ImageField(upload_to=divisions_icons_location, blank=True, null=True, )

    def __str__(self):
        return self.division.name
