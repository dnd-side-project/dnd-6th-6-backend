from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from houses.models import Invite
from houses.serializers import HouseSerializer, InviteSerializer
from users.serializers import UserSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_house(request):
    if request.user.user_profile.house:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = HouseSerializer(data=request.data)
    if serializer.is_valid():
        request.user.user_profile.house = serializer.save()
        request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def invite_member(request):
    house = request.user.user_profile.house
    if not house:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response = []
    for data in request.data:
        try:
            email = data["email"]
        except:
            return Response("email required", status=status.HTTP_400_BAD_REQUEST)

        invitee = get_object_or_404(User, username=email)
        invitee.user_profile.house = house
        invitee.user_profile.save()
    
    return Response({"message": "success"}, status=status.HTTP_201_CREATED)
    



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def accept_invite(request):
    try:
        invite_id = request.data["invite_id"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    invite = Invite.objects.get(pk=invite_id)
    if invite.invitee != request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    request.user.user_profile.house = invite.house
    request.user.user_profile.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_members(request):
    members = User.objects.filter(
        user_profile__house=request.user.user_profile.house
    ).exclude(id=request.user.id)
    serializer = UserSerializer(members, many=True)
    return Response(serializer.data)