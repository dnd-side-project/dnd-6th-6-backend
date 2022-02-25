import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
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
    notifications_notice = NotificationNotice.objects.filter(
        to=request.user
    )
    notifications_invite = NotificationInvite.objects.filter(
        invite__invitee=request.user
    )
    notifications_feedback = NotificationFeedback.objects.filter(
        to=request.user
    )
    notifications_favor = NotificationFavor.objects.filter(
        favor__to=request.user
    )
    
    notifications = []
    i, j, k, l = 0, 0, 0, 0
    while i < len(notifications_notice) or j < len(notifications_invite) or k < len(notifications_feedback) or l < len(notifications_favor):
        latest_time = datetime.datetime(1, 1, 1)
        if i < len(notifications_notice):
            notification = notifications_notice[i]
            created_at = notification.created_at
            if created_at > latest_time:
                latest = notification
                latest_time = created_at
        if j < len(notifications_invite):
            notification = notifications_invite[j]
            created_at = notification.created_at
            if notification.created_at > latest_time:
                latest = notification
                latest_time = created_at
        if k < len(notifications_feedback):
            notification = notifications_feedback[k]
            created_at = notification.created_at
            if notification.created_at > latest_time:
                latest = notification
                latest_time = created_at
        if l < len(notifications_favor):
            notification = notifications_favor[l]
            created_at = notification.created_at
            if notification.created_at > latest_time:
                latest = notification
                latest_time = created_at
        
        if type(latest) == NotificationNotice:
            notifications.append(NotificationNoticeSerializer(latest).data)
            i += 1
        elif type(latest) == NotificationInvite:
            notifications.append(NotificationInviteSerializer(latest).data)
            j += 1
        elif type(latest) == NotificationFeedback:
            notifications.append(NotificationFeedbackSerializer(latest).data)
            k += 1
        elif type(latest) == NotificationFavor:
            notifications.append(NotificationFavorSerializer(latest).data)
            l += 1
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response(notifications)

@api_view(["PATCH"])
def check_notification(request, pk):
    try:
        _type = request.GET["type"]
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if _type=="notice":
        notification = get_object_or_404(NotificationNotice, pk=pk, to=request.user)
        serializer_class = NotificationNoticeSerializer
    elif _type=="invite":
        notification = get_object_or_404(NotificationInvite, pk=pk, invite__invitee=request.user)
        serializer_class = NotificationInviteSerializer
    elif _type=="feedback":
        notification = get_object_or_404(NotificationFeedback, pk=pk, to=request.user)
        serializer_class = NotificationFeedbackSerializer
    elif _type=="favor":
        notification = get_object_or_404(NotificationFavor, pk=pk, favor__to=request.user)
        serializer_class = NotificationFavorSerializer
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    notification.is_checked = True
    notification.save()
    serializer = serializer_class(notification)
    return Response(serializer.data)