import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from .models import EmailAuth, Profile, User


# jwt 사용
# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
# from rest_framework_simplejwt.tokens import RefreshToken

# get profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)


# 회원가입시 프로필
class SignupProfileSerializer(serializers.ModelSerializer):
    signup_email = serializers.CharField(max_length=20)  # 이메일
    name = serializers.CharField(max_length=20)  # 이름

    def save(self, validated_data):
        signup_email = validated_data["signup_email"]

        user = User.objects.filter(username=signup_email)
        user.update(first_name=validated_data["name"])

        profile = Profile.objects.filter(user=user).update(
            gender=validated_data["gender"],
            avartar=validated_data["avartar"],
            life_pattern=validated_data["life_pattern"],
            disposition=validated_data["disposition"],
            mbti=validated_data["mbti"],
            message=validated_data["message"],
        )
        return profile

    class Meta:
        model = Profile
        fields = (
            "signup_email",
            "name",
            "avartar",
            "gender",
            "life_pattern",
            "disposition",
            "mbti",
            "message",
        )


# 전체 유저, 해당 유저
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source="user_profile", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",  # 회원가입한 이메일
            "first_name",  # 유저이름
            "profile",
        )


# 이메일 인증
class EmailAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAuth
        fields = ("signup_email",)

    def create(self, validated_data):
        signup_email = validated_data["signup_email"]
        code = self.__send_code(signup_email)
        emailauth = EmailAuth(signup_email=signup_email, code=code)
        emailauth.save()
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
class CreateUserSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=12, required=True)
    ck_password = serializers.CharField(min_length=8, max_length=12, required=True)

    class Meta:
        model = User
        fields = (
            "signup_email",
            "password",
            "ck_password",
        )

    def save(self, validated_data):  # 회원가입
        signup_email = validated_data["signup_email"]
        password = validated_data["password"]
        user = User(username=signup_email)
        user.set_password(password)
        user.save()
        return user

    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, **kwargs):
        if created:
            Token.objects.get_or_create(user=instance)  # 토큰 생성
            Profile.objects.create(user=instance)  # 프로필 생성
