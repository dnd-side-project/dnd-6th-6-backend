from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from houses.models import House
from houses.serializers import HouseSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_house(request):
    # if request.user.profile.house:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = HouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
