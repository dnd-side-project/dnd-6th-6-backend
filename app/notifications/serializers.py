from rest_framework import serializers

from users.serializers import UserSerializer
from notices.serializers import NoticeSerializer
from notifications.models import NotificationNotice

class NotificationNoticeSerializer(serializers.ModelSerializer):
    notice = NoticeSerializer(read_only=True)
    to = UserSerializer(read_only=True)
    
    class Meta:
        model = NotificationNotice
        fields = ["id", "notice", "to", "is_checked"]