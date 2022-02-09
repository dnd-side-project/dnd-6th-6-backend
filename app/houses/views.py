from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from houses.models import Invite
from houses.serializers import HouseSerializer, InviteSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_house(request):
    if request.user.profile.house:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = HouseSerializer(data=request.data)
    if serializer.is_valid():
        request.user.profile.house = serializer.save()
        request.user.profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def invite_member(request):
    house = request.user.profile.house
    if not house:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    email = request.data.get("email")
    if not email:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        invitee = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except User.MultipleObjectsReturned:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = InviteSerializer(
       data = {
           "house": house.id,
           "inviter": request.user.id,
           "invitee": invitee.id
       }
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    request.user.profile.house = invite.house
    request.user.profile.save()
    return Response(status=status.HTTP_200_OK)