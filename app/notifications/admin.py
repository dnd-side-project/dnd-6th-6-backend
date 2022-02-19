from django.contrib import admin

from notifications.models import NotificationNotice, NotificationInvite, NotificationFeedback

admin.site.register(NotificationNotice)
admin.site.register(NotificationInvite)
admin.site.register(NotificationFeedback)