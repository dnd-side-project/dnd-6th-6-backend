from rest_framework import serializers

from users.serializers import UserSerializer
from notices.serializers import NoticeSerializer
from houses.serializers import InviteSerializer
from notifications.models import NotificationNotice, NotificationInvite

class NotificationNoticeSerializer(serializers.ModelSerializer):
    notice = NoticeSerializer(read_only=True)
    to = UserSerializer(read_only=True)
    
    class Meta:
        model = NotificationNotice
        fields = ["id", "notice", "to", "is_checked"]

class NotifiactionInviteSerializer(serializers.ModelSerializer):
    invite = InviteSerializer(read_only=True)
    
    class Meta:
        model = NotificationInvite
        fields = ["id", "invite", "is_checked"]