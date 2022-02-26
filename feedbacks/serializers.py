from rest_framework import serializers

from chores.serializers import ChoreSerializer
from feedbacks.models import Feedback
from users.serializers import UserSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    chore = ChoreSerializer(read_only=True)
    _from = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ["id", "chore", "_from", "content", "sended_at", "emoji"]