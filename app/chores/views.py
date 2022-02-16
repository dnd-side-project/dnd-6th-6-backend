import datetime
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chores.models import Chore, RepeatChore
from chores.permissions import IsHouseMember
from chores.serializers import ChoreSerializer, ChoreInfoSerializer, RepeatChoreSerializer

def get_today():
    now = timezone.now()
    year = now.year
    month = now.month
    day = now.day

    return datetime.date(year, month, day)

class ChoreViewSet(viewsets.ModelViewSet):
    queryset = Chore.objects.all()
    serializer_class = ChoreSerializer
    permission_classes = [IsAuthenticated, IsHouseMember]

    def list(self, request, house_id, *args, **kwargs):
        today = get_today()
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(
            information__house_id=house_id,
            planned_at__gte=today
        )

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    def create(self, request, house_id, *args, **kwargs):
        try:
            information = request.data["information"]
        except:
            return Response({"message": "information required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer_for_chore_info = ChoreInfoSerializer(data=information)
        serializer_for_chore_info.is_valid(raise_exception=True)

        try:
            category = information["category"]
            category_id = category["id"]
        except:
            return Response({"message": "category required"}, status=status.HTTP_400_BAD_REQUEST)
        
        chore_info = serializer_for_chore_info.save(
            house_id=house_id,
            category_id=category_id
        )
        serializer_for_chore = self.get_serializer(data=request.data)
        serializer_for_chore.is_valid(raise_exception=True)
        
        try:
            assignees = request.data["assignees"]
        except:
            return Response({"message": "assignees required"}, status=status.HTTP_400_BAD_REQUEST)

        assignees_id = []
        for i in range(len(assignees)):
            try:
                assignees_id.append(assignees[i]["id"])
            except:
                return Response({"message": "assignees id required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(assignees_id) == 0:
            return Response({"message": "assignees 0"}, status=status.HTTP_400_BAD_REQUEST)

        serializer_for_chore.save(
            assignees=assignees_id,
            information=chore_info
        )
        
        headers = self.get_success_headers(serializer_for_chore.data)
        return Response(serializer_for_chore.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, house_id, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        try:
            information = request.data["information"]
        except:
            return Response({"message": "information required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_for_chore_info = ChoreInfoSerializer(
            instance.information,
            data=information,
            partial=partial
        )
        serializer_for_chore_info.is_valid(raise_exception=True)

        try:
            category = information["category"]
            category_id = category["id"]
        except:
            return Response({"message": "category required"}, status=status.HTTP_400_BAD_REQUEST)
        
        chore_info = serializer_for_chore_info.save(
            house_id=house_id,
            category_id=category_id
        )
        serializer_for_chore = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer_for_chore.is_valid(raise_exception=True)
        
        
        try:
            assignees = request.data["assignees"]
        except:
            return Response({"message": "assignees required"}, status=status.HTTP_400_BAD_REQUEST)

        assignees_id = []
        for i in range(len(assignees)):
            try:
                assignees_id.append(assignees[i]["id"])
            except:
                return Response({"message": "assignees id required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(assignees_id) == 0:
            return Response({"message": "assignees 0"}, status=status.HTTP_400_BAD_REQUEST)

        serializer_for_chore.save(
            assignees=assignees_id,
            information=chore_info
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(serializer_for_chore.data)
    
    @action(methods=["GET"], detail=False)
    def mine(self, request, house_id, *args, **kwargs):
        today = get_today()
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(
            information__house_id=house_id,
            assignees=request.user,
            planned_at__gte=today,
            planned_at__lte=today+datetime.timedelta(days=1)
        )

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    @action(methods=["GET"], detail=False)
    def others(self, request, house_id, *args, **kwargs):
        today = get_today()
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(
            information__house_id=house_id,
            planned_at__gte=today,
            planned_at__lte=today+datetime.timedelta(days=1)
        ).exclude(assignees=request.user)

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

    def list(self, request, house_id, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset_for_house = queryset.filter(information__house_id=house_id)

        page = self.paginate_queryset(queryset_for_house)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset_for_house, many=True)
        return Response(serializer.data)
    
    def create(self, request, house_id, *args, **kwargs):
        try:
            information = request.data["information"]
            category = information["category"]
            category_id = category["id"]
            days = request.data["days"]
            days_id = []
            for i in range(len(days)):
                days_id.append(days[i]["id"])

            assignees = request.data["assignees"]
            assignees_id = []
            for i in range(len(assignees)):
                assignees_id.append(assignees[i]["id"])
        except KeyError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_for_chore_info = ChoreInfoSerializer(data=information)
        serializer_for_chore_info.is_valid(raise_exception=True)
        chore_info = serializer_for_chore_info.save(
            house_id=house_id,
            category_id=category_id
        )
        
        serializer_for_chore = self.get_serializer(data=request.data)
        serializer_for_chore.is_valid(raise_exception=True)
        serializer_for_chore.save(
            assignees=assignees_id,
            information=chore_info,
            days=days_id
        )

        headers = self.get_success_headers(serializer_for_chore.data)
        return Response(data=serializer_for_chore.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, house_id, *args, **kwargs):
        try:
            information = request.data["information"]
            category = information["category"]
            category_id = category["id"]
            days = request.data["days"]
            days_id = []
            for i in range(len(days)):
                days_id.append(days[i]["id"])

            assignees = request.data["assignees"]
            assignees_id = []
            for i in range(len(assignees)):
                assignees_id.append(assignees[i]["id"])
        except KeyError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer_for_chore_info = ChoreInfoSerializer(
            instance.information,
            data=information,
            partial=partial
        )
        serializer_for_chore_info.is_valid(raise_exception=True)
        chore_info = serializer_for_chore_info.save(
            house_id=house_id,
            category_id=category_id
        )

        serializer_for_chore = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer_for_chore.is_valid(raise_exception=True)
        serializer_for_chore.save(
            assignees=assignees_id,
            information=chore_info,
            days=days_id
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(serializer_for_chore.data)