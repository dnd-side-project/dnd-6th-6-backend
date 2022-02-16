from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chores.models import Chore
from favor.models import Favor
from favor.serializers import FavorSerializer
from favor.permissions import IsHouseMember

class FavorViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet):

    queryset = Favor.objects.all()
    serializer_class = FavorSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def create(self, request, chore_id, *args, **kwargs):
        get_object_or_404(request.user.chores, pk=chore_id)
        
        try:
            to = request.data["to"]
            to_id = to["id"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            chore_id=chore_id,
            _from=request.user,
            to_id = to_id
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
