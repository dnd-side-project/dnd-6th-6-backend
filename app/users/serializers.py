from rest_framework import serializers
from .models import EmailAuth, Profile, User


# profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)


# user
class UserSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",  # 회원가입한 이메일
            "password",
            "first_name",  # 유저이름
            "user_profile",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    ck_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "ck_password",
        )

    def create(self, validated_data):
        username = validated_data["username"]
        pw = validated_data["password"]
        user = User.objects.create(
            username=username,  # 이메일
        )
        user.set_password(pw)
        return user


# 이메일 인증
class EmailAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAuth
        fields = ("signup_email",)
