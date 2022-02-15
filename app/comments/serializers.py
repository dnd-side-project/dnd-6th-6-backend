from rest_framework import serializers

from comments.models import CommentChore
from chores.serializers import ChoreSerializer
from users.serializers import UserSerializer

class CommentChoreSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    chore = ChoreSerializer(read_only=True)
    
    class Meta:
        model = CommentChore
        fields = ["id", "writer", "chore", "content", "writed_at"]