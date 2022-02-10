from rest_framework import serializers

from chores.models import Category, ChoreInfo, Chore
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ChoreInfoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ChoreInfo
        fields = ["id", "name", "description", "category"]


class ChoreSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    information = ChoreInfoSerializer()

    class Meta:
        model = Chore
        fields = ["id", "assignee", "information", "planned_at", "completed_at"]


class RepeatChoreSerializer(serializers.ModelSerializer):
    information = ChoreInfoSerializer()
    assignees = UserSerializer(read_only=True, many=True)