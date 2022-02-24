from django.db import models

from chores.models import Chore
from users.models import User

class Feedback(models.Model):

    class Emoji(models.IntegerChoices):
        HEART = 1
        SMILE = 2
        SAD = 3
        FIRE = 4
        GOOD = 5

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
    content = models.TextField()
    sended_at = models.DateTimeField(auto_now_add=True)
    emoji = models.SmallIntegerField(
        choices=Emoji.choices
    )
    
    class Meta:
        ordering = ["-sended_at"]