from datetime import datetime
from django.db import models
from user_app.models import BUser

class Review(models.Model):
    reviewer = models.ForeignKey(BUser, on_delete=models.CASCADE)
    reviewee = models.ForeignKey(BUser, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    created_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)
    updated_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)

    def __str__(self):
        return f"review by {self.reviewer.name} on {self.reviewee.name}"
