import uuid
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import EmailAuth, Profile, User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage


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


# 이메일 인증
class EmailAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAuth
        fields = ("signup_email",)

    def create(self, validated_data):
        signup_email = validated_data["signup_email"]
        code = self.__send_code(signup_email)
        emailauth = EmailAuth.objects.create(signup_email=signup_email, code=code)
        return emailauth

    # 인증코드 전송
    def __send_code(self, auth_email):
        code = str(uuid.uuid4())[:6]  # 초대코드
        auth_email = EmailMessage(
            "Rountable 회원가입 인증코드",  # 제목
            "인증코드: " + code,  # 본문
            to=[auth_email],  # 수신자 이메일
        )
        auth_email.send()
        return code


# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    signup_email = serializers.CharField(max_length=20)
    ck_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = (
            "signup_email",
            "password",
            "ck_password",
        )

    def create(self, validated_data):
        signup_email = validated_data["signup_email"]
        pw = validated_data["password"]
        hashed_pw = make_password(pw)
        user = User.objects.create_user(username=signup_email, password=hashed_pw)
        Token.objects.create(user=user)  # 토큰 생성
        Profile.objects.create(user=user)
        return user


# 로그인
class TokenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
