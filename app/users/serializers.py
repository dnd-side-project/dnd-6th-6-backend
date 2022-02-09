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
            "first_name",  # 유저이름
        )


# profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

    @classmethod
    def setup_preloading(cls, queryset):
        return queryset.select_related("user")  # join
