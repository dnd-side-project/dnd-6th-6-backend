from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chores.models import Chore, RepeatChore
from chores.permissions import IsHouseMember
from chores.serializers import ChoreSerializer, ChoreInfoSerializer, RepeatChoreSerializer


class ChoreViewSet(viewsets.ModelViewSet):
    queryset = Chore.objects.all()
    serializer_class = ChoreSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(assignee__user_profile__house=request.user.user_profile.house)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        information = request.data.get("information", dict())
        serializer_for_chore_info = ChoreInfoSerializer(data=information)
        serializer_for_chore_info.is_valid(raise_exception=True)
        category = information.get("category", {"id":1})
        chore_info = serializer_for_chore_info.save(category_id=category["id"])
        
        serializer_for_chore = self.get_serializer(data=request.data)
        serializer_for_chore.is_valid(raise_exception=True)
        assignee = request.data.get("assignee", {"id":request.user.id})
        serializer_for_chore.save(
            assignee_id=assignee["id"],
            information=chore_info
        )
        
        headers = self.get_success_headers(serializer_for_chore.data)
        return Response(serializer_for_chore.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        information = request.data.get("information", dict())
        serializer_for_chore_info = ChoreInfoSerializer(
            instance.information,
            data=information,
            partial=partial
        )
        serializer_for_chore_info.is_valid(raise_exception=True)
        category = information.get("category", {"id": 1})
        chore_info = serializer_for_chore_info.save(category_id=category["id"])

        serializer_for_chore = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer_for_chore.is_valid(raise_exception=True)
        assignee = request.data.get("assignee", {"id": instance.assignee.id})
        serializer_for_chore.save(
            assignee_id=assignee["id"],
            information=chore_info
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(serializer_for_chore.data)
    
    @action(methods=["GET"], detail=False)
    def mine(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(
            assignee__user_profile__house=request.user.user_profile.house
        ).filter(assignee=request.user)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    @action(methods=["GET"], detail=False)
    def others(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(
            assignee__user_profile__house=request.user.user_profile.house
        ).exclude(assignee=request.user)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)


class RepeatChoreViewSet(viewsets.ModelViewSet):
    queryset = RepeatChore.objects.all()
    serializer_class = RepeatChoreSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(assignees__user_profile__house=request.user.user_profile.house)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)