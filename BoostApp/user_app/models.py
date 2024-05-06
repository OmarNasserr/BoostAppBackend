from django.db import models

from django.contrib.auth.models import AbstractUser

class BUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_booster = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)
