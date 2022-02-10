import uuid
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
        code = str(uuid.uuid4())[:6] 
        email_user = EmailAuth.objects.create(signup_email=email, code=code)
        return email_user

    # private
    def __send_code(self):
        pass


    class Meta:
        model = EmailAuth
        fields = "__all__"
