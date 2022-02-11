from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import EmailAuth, Profile, User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password


# jwt 사용
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# from rest_framework_simplejwt.tokens import RefreshToken


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
            "first_name",  # 유저이름
            "user_profile",
        )


# 회원가입
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
        hashed_pw = make_password(pw)
        user = User.objects.create_user(username=username, password=hashed_pw)  # 이메일
        Token.objects.create(user=user)
        return user


# 로그인
class TokenUserSerializer(serializers.ModelSerializer):
    login_id = serializers.CharField(max_length=20)
    login_pw = serializers.CharField(max_length=50)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        login_id = data["login_id"]
        pw = data["login_pw"]
        user = authenticate(username=login_id, password=pw)

        if user is None:
            return {"login_id": "None"}
        else:
            # payload = JWT_PAYLOAD_HANDLER(user)
            # jwt_token = JWT_ENCODE_HANDLER(payload)
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            # update_last_login(None, user)

            return {"login_id": user.username, "token": token.key}

    class Meta:
        model = User
        fields = (
            "login_id",
            "login_pw",
            "token",
        )


# 이메일 인증
class EmailAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAuth
        fields = ("signup_email",)
