from rest_framework import serializers

from favor.models import Favor
from chores.serializers import ChoreSerializer
from users.serializers import UserSerializer

class FavorSerializer(serializers.ModelSerializer):
    chore = ChoreSerializer(read_only=True)
    _from = UserSerializer(read_only=True)
    to = UserSerializer(read_only=True)

    class Meta:
        model = Favor
        fields = ["id", "chore", "_from", "to", "content", "sended_at"]