from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from chores.models import Chore, Category
from chores.serializers import ChoreSerializer, ChoreInfoSerializer

class ChoreViewSet(viewsets.ModelViewSet):
    queryset = Chore.objects.all()
    serializer_class = ChoreSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(assignee__profile__house=request.user.profile.house)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        information = request.data.get("information")
        serializer_for_chore_info = ChoreInfoSerializer(data=information)
        serializer_for_chore_info.is_valid(raise_exception=True)
        category_id = information.get("category_id", 1)
        chore_info = serializer_for_chore_info.save(category_id=category_id)
        
        serializer_for_chore = self.get_serializer(data=request.data)
        serializer_for_chore.is_valid(raise_exception=True)
        assignee_id = request.data.get("assignee_id", request.user.id)
        serializer_for_chore.save(
            assignee_id=assignee_id,
            information=chore_info
        )
        
        headers = self.get_success_headers(serializer_for_chore.data)
        return Response(serializer_for_chore.data, status=status.HTTP_201_CREATED, headers=headers)