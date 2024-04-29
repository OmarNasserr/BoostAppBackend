from django.db import models

from django.contrib.auth.models import AbstractUser

class BUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
