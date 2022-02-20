from rest_framework import serializers

from notices.models import Notice
from users.serializers import UserSerializer

class NoticeSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    class Meta:
        model = Notice
        fields = ["id", "writer", "title", "content", "writed_at", "updated_at"]