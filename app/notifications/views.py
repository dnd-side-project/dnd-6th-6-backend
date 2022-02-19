from rest_framework.decorators import api_view
from rest_framework.response import Response

from notifications.models import (
    NotificationNotice,
    NotificationInvite,
    NotificationFeedback,
    NotificationFavor
)
from notifications.serializers import (
    NotificationNoticeSerializer,
    NotificationInviteSerializer,
    NotificationFeedbackSerializer,
    NotificationFavorSerializer
)


@api_view(["GET"])
def get_notifications(request):
    notifications_queryset = NotificationNotice.objects.filter(
        to=request.user
    )
    notifications_queryset.union(
        NotificationInvite.objects.filter(
            invite__invitee=request.user
        ),
        NotificationFeedback.objects.filter(
            to=request.user
        ),
        NotificationFavor.objects.filter(
            favor__to=request.user
        )
    ).order_by('-created_at')

    notifications = []
    for notification in notifications_queryset:
        if type(notification) == NotificationNotice:
            notifications.append(NotificationNoticeSerializer(notification).data)
        elif type(notification) == NotificationInvite:
            notifications.append(NotificationInviteSerializer(notification).data)
        elif type(notification) == NotificationFeedback:
            notifications.append(NotificationFeedbackSerializer(notification).data)
        elif type(notification) == NotificationFavor:
            notifications.append(NotificationFavorSerializer(notification).data)
    
    return Response(notifications)