from rest_framework import serializers

from houses.models import House, Invite
from users.serializers import UserSerializer

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["id", "name", "created_at"]


class InviteSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)
    inviter = UserSerializer(read_only=True)
    invitee = UserSerializer(read_only=True)
    
    class Meta:
        model = Invite
        fields = ["id", "house", "inviter", "invitee", "sended_at"]