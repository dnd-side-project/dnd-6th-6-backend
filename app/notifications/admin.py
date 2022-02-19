from django.contrib import admin

from notifications.models import NotificationNotice, NotificationInvite

admin.site.register(NotificationNotice)
admin.site.register(NotificationInvite)