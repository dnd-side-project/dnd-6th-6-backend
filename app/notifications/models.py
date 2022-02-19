from django.db import models

from notices.models import Notice
from users.models import User
from houses.models import Invite
from feedbacks.models import Feedback
from favor.models import Favor

class NotificationNotice(models.Model):
    notice = models.ForeignKey(
        Notice,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification"
    )
    to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications_notice",
        related_query_name="notification_notice"
    )
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-notice__writed_at"]

class NotificationInvite(models.Model):
    invite = models.ForeignKey(
        Invite,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notificatoin"
    )
    is_checked = models.BooleanField(default=True)

    class Meta:
        ordering = ["-invite__sended_at"]

class NotificationFeedback(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification"
    )
    is_checked = models.BooleanField(default=True)

    class Meta:
        ordering = ["-feedback__sended_at"]

class NotificationFavor(models.Model):
    favor = models.ForeignKey(
        Favor,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification"
    )
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-favor__sended_at"]