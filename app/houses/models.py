from django.contrib.auth.models import User
from django.db import models


class House(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Invite(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="invites",
        related_query_name="invite"
    )
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="invite",
        related_query_name="invite"
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="invited",
        related_query_name="invited"
    )
    sended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inviter} invited {self.invitee} to {self.house}"