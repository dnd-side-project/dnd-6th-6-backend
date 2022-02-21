import uuid, re
from wsgiref import validate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import EmailAuth, Profile, User, SocialUser
from rest_framework.exceptions import ValidationError


##회원가입-프로필##
class SignupProfileSerializer(serializers.ModelSerializer):
    signup_email = serializers.CharField(max_length=20)  # 이메일
    name = serializers.CharField(max_length=10)  # 이름

    def create(self, validated_data):
        signup_email = validated_data["signup_email"]
        user = User.objects.filter(username=signup_email)
        user.update(first_name=validated_data["name"])

        return user

    class Meta:
        model = Profile
        fields = (
            "signup_email",
            "name",
        )


# get user
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "house",
        )


##전체 유저, 해당 유저 조회 ##
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


##회원가입-이메일 인증##
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


##회원가입-패스워드##
class CreateUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, required=True)
    ck_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = (
            "signup_email",
            "password",
            "ck_password",
        )

    def validate(self, data):
        pw = data["password"]
        ck_pw = data["ck_password"]

        if pw != ck_pw:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        elif len(pw) < 8 or len(pw) > 20:
            raise ValidationError("비밀번호는 8자리 이상 20자리 이하로 설정해주십시오.")
        elif not (
            re.findall("[0-9]", pw)
            and (re.findall("[a-z]", pw) or re.findall("[A-Z]", pw))
            and re.findall("[`~!@#$%^&*()_=-+[]?/<>,.]", pw)
        ):
            raise ValidationError("최소 1개 이상의 숫자, 영문자, 특수 문자를 포함해 주십시오")
        else:
            return data

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
            Token.objects.create(user=instance)  # 토큰 생성
            Profile.objects.create(user=instance)  # 프로필 생성
