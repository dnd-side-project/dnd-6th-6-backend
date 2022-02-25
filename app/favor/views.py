from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chores.models import Chore
from favor.models import Favor
from favor.serializers import FavorSerializer
from favor.permissions import IsHouseMember

class FavorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
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
    
    def list(self, request, chore_id, *args, **kwargs):
        try:
            start_dt = request.GET["start_dt"]
            end_dt = request.GET["end_dt"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(
            _from=request.user,
            sended_at__gte=start_dt,
            sended_at__lte=end_dt
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=["PATCH"], detail=True)
    def accept(self, request, chore_id, *args, **kwargs):
        instance = self.get_object()
        if instance.to != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        instance.chore.assignees.add(instance.to)
        instance.chore.assignees.remove(instance._from)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)