from dataclasses import field
from rest_framework import serializers
from .models import Profile, User


# user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",  # 회원가입한 이메일
            "first_name",
            "profile",  # 유저이름
        )


# profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
