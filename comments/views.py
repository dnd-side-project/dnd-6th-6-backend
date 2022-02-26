from rest_framework import mixins
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import CommentChore, CommentRepeatChore
from comments.permissions import IsHouseMember
from comments.serializers import CommentChoreSerializer, CommentRepeatChoreSerializer

class CommentChoreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    queryset = CommentChore.objects.all()
    serializer_class = CommentChoreSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def list(self, request, chore_id, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(chore_id=chore_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, chore_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            writer=request.user,
            chore_id=chore_id
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentRepeatChoreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    queryset = CommentRepeatChore.objects.all()
    serializer_class = CommentRepeatChoreSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def list(self, request, repeat_chore_id, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(repeat_chore_id=repeat_chore_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, repeat_chore_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            writer=request.user,
            repeat_chore_id=repeat_chore_id
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

