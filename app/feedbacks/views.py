from rest_framework import mixins
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from feedbacks.models import Feedback
from feedbacks.permissions import IsHouseMember
from feedbacks.serializers import FeedbackSerializer

class FeedbackViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def create(self, request, chore_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            chore_id=chore_id,
            _from=request.user
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
            chore__assignees=request.user,
            sended_at__gte=start_dt,
            sended_at__lte=end_dt
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
