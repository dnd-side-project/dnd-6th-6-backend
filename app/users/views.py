from app.settings import SOCIAL_OUTH_CONFIG
from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserSerializer,
    EmailAuthSerializer,
    CreateUserSerializer,
    SignupProfileSerializer,
    ProfileSerializer,
)
from .models import EmailAuth, Profile

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


##회원가입##
# 1. 인증코드 전송 이메일 - 회원 가입, 비밀번호 찾기
@api_view(["POST"])
@permission_classes([AllowAny])
def auth_email(request):  # signtup_email
    serializer = EmailAuthSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)  # 전송
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. 인증코드 인증
@api_view(["POST"])
@permission_classes([AllowAny])
def auth_code(request):  # request code
    code = request.data["code"]
    auth_code = EmailAuth.objects.filter(code=code)

    if (auth_code is not None) and (auth_code.using):
        auth_code.update(using=False)

        return Response(
            data={"signup_email": auth_code[0].signup_email},
            status=status.HTTP_200_OK,
        )  # 인증성공
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # 실패


# {"signup_email":"test2@email.com","password":"xptmxmdlqslek","ck_password":"xptmxmdlqslek"}
# 3. 패스워드 입력 - 회원가입, 비밀번호 찾기
@api_view(["POST"])
@permission_classes([AllowAny])
def password(request):  # request signup_email , password, ck_password
    serializer = CreateUserSerializer(data=request.data)
    pw = request.data["password"]
    ck_pw = request.data["ck_password"]

    if pw == ck_pw:
        if serializer.is_valid(raise_exception=True):
            serializer.save(request.data)
            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data="비밀번호가 불일치합니다.", status=status.HTTP_400_BAD_REQUEST)  # 실패


# 4. 프로필 입력
@api_view(["POST"])
@permission_classes([AllowAny])
def profile(request):
    serializer = SignupProfileSerializer(data=request.data)
    # request signup_email, name, gender
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)  # 성공
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {"login_email":"test3@email.com","password":"xptmxmdlqslek"}
##로그인##
@api_view(["POST"])
@permission_classes([AllowAny])
def login_email(request):
    login_email = request.data["login_email"]
    return Response(data={"login_email": login_email}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_password(request):  # request login_email, password
    login_email = request.data["login_email"]
    login_password = request.data["password"]

    user = authenticate(username=login_email, password=login_password)

    if user is not None:
        # login(request, user=user)
        token = Token.objects.get_or_create(user=user)
        to = f"Authorization: Token  {token[0].key}"
        headers = {"Authorization": to}

        return Response(
            data={"token": token[0].key}, status=status.HTTP_200_OK, headers=headers
        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


##로그아웃##
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(data="로그아웃 성공", status=status.HTTP_200_OK)


##소셜 로그인##
from django.shortcuts import redirect
import requests

NAVER_CLIENT_ID = SOCIAL_OUTH_CONFIG["NAVER_REST_API_KEY"]
NAVER_CALLBACK_URL = SOCIAL_OUTH_CONFIG["NAVER_REDIRECT_URI"]
NAVER_CLIENT_SECRET = SOCIAL_OUTH_CONFIG["NAVER_SECRET_KEY"]

KAKAO_REST_API_KEY = SOCIAL_OUTH_CONFIG["KAKAO_REST_API_KEY"]
KAKAO_REDIRECT_URI = SOCIAL_OUTH_CONFIG["KAKAO_REDIRECT_URI"]


@api_view(["GET"])
@permission_classes([AllowAny])
def naver_login(request):
    ##Code Request##
    url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={NAVER_CLIENT_ID}&&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URL}"
    return redirect(url)


@api_view(["GET"])
@permission_classes([AllowAny])
def naver_callback(request):
    ##Access Token Request##
    if "error" in request.query_params:
        return Response(data="에러 발생", status=status.HTTP_400_BAD_REQUEST)

    code = request.query_params["code"]
    url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&code={code}"
    code_response = requests.post(url)
    token_json = code_response.json()
    userUrl = "https://openapi.naver.com/v1/nid/me"  # 유저 정보 조회
    auth = "Bearer " + token_json["access_token"]
    headers = {
        "Authorization": auth,
    }

    ##Profile Request##
    response = requests.get(userUrl, headers=headers)
    profile = response.json().get("response")

    name = profile.get("name")  # 이름
    gender = profile.get("gender")  # F/M
    email = profile.get("email")  # email
    avartar = profile.get("profile_image")  # link

    try:  # 로그인
        user = USERS.objects.get(username=email)
        token = Token.objects.get_or_create(user=user)

        return Response(
            data={"token": token[0].key},
            status=status.HTTP_200_OK,
        )

    except USERS.DoesNotExist:  # 회원가입
        user = USERS.objects.create_user(username=email, first_name=name)
        Profile.objects.filter(user=user).update(gender=gender, avartar=avartar)

        return Response(
            data={"token": token[0].key},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_login(request):
    ##Code Request##
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    return redirect(url)


@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_callback(request):
    ##Access Token Request##
    code = request.query_params["code"]  # 인가 코드
    url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}"
    codeResponse = requests.post(url)
    tokenJson = codeResponse.json()

    profileUrl = "https://kapi.kakao.com/v2/user/me"  # 유저 정보 조회하는 uri
    auth = "Bearer " + tokenJson["access_token"]
    headers = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    ##Profile Request##
    response = requests.get(profileUrl, headers=headers)
    profile_json = response.json()
    profile = profile_json.get("kakao_account")

    if profile["has_email"]:  # true
        email = profile["email"]
    if profile["has_gender"]:
        gender = profile["gender"]  # female, male

    name = profile["profile"]["nickname"]

    try:  # 로그인
        user = USERS.objects.get(username=email)
        token = Token.objects.get_or_create(user=user)

        return Response(
            data={"token": token[0].key},
            status=status.HTTP_200_OK,
        )

    except USERS.DoesNotExist:  # 회원가입
        user = USERS.objects.create_user(username=email, first_name=name)
        Profile.objects.filter(user=user).update(gender=gender)

        return Response(
            data={"token": token[0].key},
            status=status.HTTP_200_OK,
        )


##마이페이지 - 프로필##
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def mypage_profile(request):
    if request.method == "GET":  # 조회
        profile = request.user.user_profile
        serializer = ProfileSerializer(profile)
        token = "6862bc494c776a6751a523a1f521420e25fcad3a"
        headers = f"Authorization: Token  {token}"
        return Response(serializer.data, headers=headers)

    elif request.method == "PATCH":  # 수정
        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)  # 성공
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# test
class TestViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
