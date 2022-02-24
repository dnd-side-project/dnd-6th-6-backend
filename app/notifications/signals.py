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
from users.models import Profile

@receiver(post_save, sender=Notice)
def create_notification_notice(sender, instance, created, **kwargs):
    if created:
        profiles = Profile.objects.filter(house=instance.house)
        for profile in profiles:
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
def create_notification_feedback(sender, instance, created, **kwargs):
    if created:
        for assignee in instance.chore.assignees.all():
            notification = NotificationFeedback(feedback=instance, to=assignee)
            notification.save()

@receiver(post_save, sender=Favor)
def create_notification_favor(sender, instance, created, **kwargs):
    if created:
        notification = NotificationFavor(favor=instance)
        notification.save()