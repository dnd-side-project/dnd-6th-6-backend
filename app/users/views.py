from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    EmailAuthSerializer,
    CreateUserSerializer,
    SignupProfileSerializer,
)

from .models import EmailAuth

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


# 1. 이메일 입력, 인증 코드 전송
class EmailAuthSet(viewsets.ModelViewSet):
    queryset = EmailAuth.objects.all()
    serializer_class = EmailAuthSerializer


# 2. 인증코드 인증
@api_view(["POST"])
def auth_code(request):  # request code
    code = request.data["code"]
    auth_code = EmailAuth.objects.filter(code=code)

    if (auth_code is not None) and (auth_code.using):
        auth_code.update(using=False)

        return Response(
            data={
                "signup_email": auth_code.signup_email,
            },
            status=status.HTTP_200_OK,
        )  # 인증성공
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # 실패


# {"signup_email":"test2@email.com","password":"xptmxmdlqslek","ck_password":"xptmxmdlqslek"}
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
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# 4. 프로필 입력
@api_view(["POST"])
def profile(request):
    serializer = SignupProfileSerializer(data=request.data)

    if request.method == "POST":  # request signup_email, name, profile
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {"login_email":"test2@email.com","password":"xptmxmdlqslek"}
# 로그인
@api_view(["POST"])
def log_in(request):
    if request.method == "POST":
        login_id = request.data["login_email"]
        login_pw = request.data["password"]

        user = authenticate(username=login_id, password=login_pw)

        if user is not None:
            login(request, user=user)
            # token = Token.objects.get(user=user)
            return Response(data="로그인 성공", status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def log_out(request):
    logout(request)
    return Response(data="로그아웃 성공", status=status.HTTP_200_OK)


# @authentication_classes([authentication.TokenAuthentication])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response({"user": request.user}, status=200)
