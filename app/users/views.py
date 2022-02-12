from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    EmailAuthSerializer,
    CreateUserSerializer,
    TokenUserSerializer,
    SignupProfileSerializer,
)

from .models import Profile, EmailAuth

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


# 1. 이메일 입력, 인증 코드 전송
class EmailAuthSet(viewsets.ModelViewSet):
    queryset = EmailAuth.objects.all()
    serializer_class = EmailAuthSerializer

    # 인증받을 이메일
    def perform_create(self, serializer):  # request signup_email
        serializer.validated_data["signup_email"]
        serializer.save()
        return Response(
            status=status.HTTP_200_OK,
        )


# 2. 인증코드 인증
@api_view(["POST"])
def auth_code(request):  # request code
    code = request.data["code"]
    auth_code = EmailAuth.objects.get(code=code)

    if auth_code is not None:
        auth_code
        return Response(
            data={
                "signup_email": auth_code.signup_email,
            },
            status=status.HTTP_200_OK,
        )  # 인증성공
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # 실패


# 3. 회원가입
@api_view(["POST"])
def sign_up(request):  # request signup_email , password, ck_password
    serializer = CreateUserSerializer(data=request.data)
    pw = request.data["password"]
    ck_pw = request.data["ck_password"]

    if pw == ck_pw:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # 실패


# 프로필 입력
@api_view(["POST"])
def profile(request):
    serializer = SignupProfileSerializer(data=request.data)

    if request.method == "POST":  # request signup_email, name, profile
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
@api_view(["POST"])
def log_in(request):
    login_id = request.data["username"]
    login_pw = request.data["password"]

    user = authenticate(username=login_id, password=login_pw)

    if user is not None:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenUserSerializer

    @action(detail=False, methods=["POST"])
    def log_in(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_409_CONFLICT)
        if serializer.validated_data["login_id"] == "None":
            return Response(data="로그인 실패", status=status.HTTP_400_BAD_REQUEST)

        response = {"success": "True", "token": serializer.data["token"]}
        return Response(response, status=status.HTTP_200_OK)
"""
