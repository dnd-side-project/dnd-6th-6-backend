from rest_framework import serializers

from chores.models import Category, ChoreInfo, Chore, Day,RepeatChore
from houses.serializers import HouseSerializer
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ChoreInfoSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ChoreInfo
        fields = ["id", "name", "description", "house", "category"]


class ChoreSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    information = ChoreInfoSerializer()

    class Meta:
        model = Chore
        fields = ["id", "assignee", "information", "planned_at", "completed_at"]


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ["id", "name"]

class RepeatChoreSerializer(serializers.ModelSerializer):
    information = ChoreInfoSerializer()
    assignees = UserSerializer(read_only=True, many=True)
    days = DaySerializer(read_only=True, many=True)

    class Meta:
        model = RepeatChore
        fields = ["information", "assignees", "days"]