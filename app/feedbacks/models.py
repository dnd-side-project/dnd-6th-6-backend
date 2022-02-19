from django.db import models

from chores.models import Chore
from users.models import User

class Feedback(models.Model):
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedback"
    )
    _from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback",
        related_query_name="has_feedback"
    )
    content = models.CharField(max_length=255)
    sended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chore}: {self.title}"
    
    class Meta:
        ordering = ["-sended_at"]