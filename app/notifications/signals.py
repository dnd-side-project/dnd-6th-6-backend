from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import (
    NotificationNotice,
    NotificationInvite,
    NotificationFeedback,
    NotificationFavor
)
from notices.models import Notice
from houses.models import Invite
from feedbacks.models import Feedback
from favor.models import Favor

@receiver(post_save, sender=Notice)
def create_notification_notice(sender, instance, created, **kwargs):
    if created:
        for profile in instance.house.profile.all():
            if profile.user == instance.writer:
                continue
            notification = NotificationNotice(notice=instance, to=profile.user)
            notification.save()
            
@receiver(post_save, sender=Invite)
def create_notification_invite(sender, instance, created, **kwargs):
    if created:
        notification = NotificationInvite(invite=instance)
        notification.save()

@receiver(post_save, sender=Feedback)
def create_notification_notice(sender, instance, created, **kwargs):
    if created:
        for assignee in instance.chore.assignees.all():
            notification = NotificationFeedback(Feedback=instance, to=assignee)
            notification.save()