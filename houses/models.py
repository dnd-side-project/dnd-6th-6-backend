from django.contrib.auth.models import User
from django.db import models


class House(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invite(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="invites",
        related_query_name="invite",
    )
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invites",
        related_query_name="sent_invite",
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invites",
        related_query_name="received_invite",
    )
    sended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inviter} invited {self.invitee} to {self.house}"
    
    class Meta:
        ordering = ["-sended_at"]
