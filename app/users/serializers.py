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
    # name = serializers.CharField(max_length=20)  # 이름

    def save(self):
        signup_email = self.validated_data["signup_email"]
        # name = self.validated_data["name"]

        # gender = self.validated_data["gender"]
        # avatar = models.ImageField(blank=True)
        # life_pattern = self.validated_data["life_pattern"]
        # disposition = self.validated_data["disposition"]
        # mbti = self.validated_data["mbti"]
        message = self.validated_data["message"]

        user = User.objects.get(username=signup_email)
        # user.update(first_name=name)

        profile = Profile.objects.filter(user=user).update(  # 역참조
            # gender=gender,
            # life_pattern=life_pattern,
            # disposition=disposition,
            # mbti=mbti,
            message=message,
        )
        return profile

    class Meta:
        model = Profile
        fields = (
            "signup_email",
            # "name",
            # "gender",
            # "life_pattern",
            # "disposition",
            # "mbti",
            "message",
        )


# user
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
class CreateUserSerializer(serializers.Serializer):
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
        Profile.objects.create(user=user)  # 프로필 생성
        return user


# 로그인
class TokenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
