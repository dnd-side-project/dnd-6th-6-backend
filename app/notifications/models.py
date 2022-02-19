from django.db import models

from notices.models import Notice
from users.models import User

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