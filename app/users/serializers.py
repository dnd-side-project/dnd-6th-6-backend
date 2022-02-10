import uuid
from django.core.mail import EmailMessage
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


# 이메일 인증
class EmailAuthSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        email = validated_data.get("signup_email")
        code = str(uuid.uuid4())[:6]  # 초대코드
        email_user = EmailAuth.objects.create(signup_email=email, code=code)
        email_user.save()
        self.__send_code(code, email)
        return validated_data

    # 인증코드 전송
    def __send_code(self, code, email):
        email = EmailMessage(
            "Rountable 회원가입 인증코드",  # 제목
            "인증코드: " + code,  # 본문
            to=[email],  # 수신자 이메일
        )
        email.send()

    class Meta:
        model = EmailAuth
        fields = "__all__"
