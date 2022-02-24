from django.contrib import admin

from notifications.models import NotificationNotice, NotificationInvite, NotificationFeedback, NotificationFavor

admin.site.register(NotificationNotice)
admin.site.register(NotificationInvite)
admin.site.register(NotificationFeedback)
admin.site.register(NotificationFavor)