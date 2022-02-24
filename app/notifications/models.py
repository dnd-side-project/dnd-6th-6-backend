from django.db import models

from notices.models import Notice
from users.models import User
from houses.models import Invite
from feedbacks.models import Feedback
from favor.models import Favor

class Notification(models.Model):
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

class NotificationNotice(Notification):
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

class NotificationInvite(Notification):
    invite = models.OneToOneField(
        Invite,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notificatoin"
    )

class NotificationFeedback(Notification):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification"
    )
    to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications_feedback",
        related_query_name="notification_feedback"
    )

class NotificationFavor(Notification):
    favor = models.OneToOneField(
        Favor,
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification"
    )