from django.db import models

from chores.models import Chore
from users.models import User

class Favor(models.Model):
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="favor",
        related_query_name="favor"
    )
    _from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favor_sended",
        related_query_name="favor_sended"
    )
    to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favor_received",
        related_query_name="favor_received"
    )
    content = models.CharField(max_length=255)
    sended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sended_at"]