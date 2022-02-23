from rest_framework import serializers

from comments.models import CommentChore, CommentRepeatChore
from users.serializers import UserSerializer

class CommentChoreSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentChore
        fields = ["id", "writer", "chore", "content", "writed_at"]

class CommentRepeatChoreSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentRepeatChore
        fields = ["id", "writer", "repeat_chore", "content", "writed_at"]