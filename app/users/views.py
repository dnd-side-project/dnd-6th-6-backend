import uuid
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, EmailAuthSerializer
from .models import Profile, EmailAuth

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


class EmailAuthSet(viewsets.ModelViewSet):  # POST
    queryset = EmailAuth.objects.all()
    serializer_class = EmailAuthSerializer

    # post users/email
    def perform_create(self, serializer):
        signup_email = serializer.validated_data["signup_email"]
        code = self.__send_code(signup_email)
        serializer.save(code=code)

    # 인증코드 전송
    def __send_code(self, email):
        code = str(uuid.uuid4())[:6]  # 초대코드
        email = EmailMessage(
            "Rountable 회원가입 인증코드",  # 제목
            "인증코드: " + code,  # 본문
            to=[email],  # 수신자 이메일
        )
        email.send()
        return code
