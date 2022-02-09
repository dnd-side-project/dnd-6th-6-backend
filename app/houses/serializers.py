from rest_framework import serializers

from houses.models import House, Invite


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["id", "name"]


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ["id", "house", "inviter", "invitee", "sended_at"]