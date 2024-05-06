from django.db import models
from user_app.models import BUser
from games_app.models import Game
from divisions_app.models import Division


class BoostingRequest(models.Model):
    player_id = models.ForeignKey(BUser, on_delete=models.CASCADE, related_name='boosting_requests')
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    current_division_id = models.ForeignKey(Division, on_delete=models.CASCADE,
                                            related_name='current_division')
    desired_division_id = models.ForeignKey(Division, on_delete=models.CASCADE,
                                            related_name='desired_division')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
