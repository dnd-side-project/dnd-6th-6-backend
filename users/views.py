from app.settings import SOCIAL_OUTH_CONFIG
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserSerializer,
    EmailAuthSerializer,
    CreateUserSerializer,
    SignupProfileSerializer,
    ProfileSerializer,
    send_code,
)
from .models import EmailAuth, Profile

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


##회원가입##
# 1. 인증코드 전송 이메일 - 회원 가입
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_email(request):  # signtup_email
    serializer = EmailAuthSerializer(data=request.data)
    user = USERS.objects.filter(username=request.data["signup_email"])

    if user.count() == 1:
        return Response(
            data={"error": "이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)  # 전송
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## 인증코드 전송 - 비밀번호 찾기##
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def find_password_email(request):  # login_email
    login_email = request.data["login_email"]
    send_code(login_email)
    return Response(status=status.HTTP_200_OK)


# 2. 인증코드 인증
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_code(request):  # request code
    code = request.data["code"]
    auth_code = EmailAuth.objects.filter(code=code)

    if code.__eq__(""):
        return Response(
            data={"error": "인증코드를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST
        )  # 실패

    if (auth_code.count() == 1) and (auth_code.using):
        auth_code.update(using=False)

        return Response(
            data={"signup_email": auth_code[0].signup_email},
            status=status.HTTP_200_OK,
        )  # 인증성공
    else:
        return Response(
            data={"error": "인증코드를 다시 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
        )  # 실패


# {"signup_email":"tester","password":"xptmxj1234!","ck_password":"xptmxj1234!"}
# 3. 패스워드 입력 - 회원가입, 비밀번호 찾기
@api_view(["POST", "PUT"])
@authentication_classes([])
@permission_classes([AllowAny])
def password(request):  # request signup_email , password, ck_password
    serializer = CreateUserSerializer(data=request.data)

    if request.method == "POST":
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 유효성 검사

            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:  # PUT
        if serializer.is_valid(raise_exception=True):
            user = USERS.objects.filter(username=request.data["signup_email"])
            hash_pw = make_password(request.data["password"])
            user.update(password=hash_pw)
            return Response(status=status.HTTP_200_OK)  # 성공
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4. 프로필 입력 - 이름
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def profile(request):
    serializer = SignupProfileSerializer(data=request.data)

    # request signup_email, name
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = USERS.objects.filter(username=request.data["signup_email"])[0]
    user_ser = UserSerializer(user)
    token = Token.objects.get_or_create(user=user)

    return Response(
        data={"token": token[0].key, "user": user_ser.data},
        status=status.HTTP_200_OK,
    )  # 성공


##로그인##
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login_email(request):
    login_email = request.data["login_email"]
    user = USERS.objects.filter(username=login_email)

    if login_email.__eq__(""):
        return Response(
            data={"error": "로그인 할 이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
        )

    if user.count() == 1:
        return Response(
            data={"login_email": login_email},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            data={"error": "존재하지 않은 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login_password(request):  # request login_email, password
    login_email = request.data["login_email"]
    login_password = request.data["password"]

    if login_password.__eq__(""):  # 비밀번호 빈칸
        return Response(
            data={"error": "비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
        )

    else:
        user = authenticate(username=login_email, password=login_password)
        user_ser = UserSerializer(user)

        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return Response(
                data={"token": token[0].key, "user": user_ser.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"error": "비밀번호를 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )


##로그아웃##
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(data="로그아웃 성공", status=status.HTTP_200_OK)


##소셜 로그인##
import requests
from django.shortcuts import redirect
from django.core.files.base import ContentFile

NAVER_CLIENT_ID = SOCIAL_OUTH_CONFIG["NAVER_REST_API_KEY"]
NAVER_CALLBACK_URL = SOCIAL_OUTH_CONFIG["NAVER_REDIRECT_URI"]
NAVER_CLIENT_SECRET = SOCIAL_OUTH_CONFIG["NAVER_SECRET_KEY"]

KAKAO_REST_API_KEY = SOCIAL_OUTH_CONFIG["KAKAO_REST_API_KEY"]
KAKAO_REDIRECT_URI = SOCIAL_OUTH_CONFIG["KAKAO_REDIRECT_URI"]


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def naver_login(request):
    ##Code Request##
    url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={NAVER_CLIENT_ID}&&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URL}"
    return redirect(url)


from urllib.parse import urlparse


@api_view(["GET"])
@authentication_classes([])
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
    email = profile.get("email")  # email

    avatar_url = profile.get("profile_image")  # url
    avatar = urlparse(avatar_url).path.split("/")[-1]  # url에서 이미지 추출
    avatar_response = requests.get(avatar_url)

    # return Response(data={"name": name, "email": email, "avatar": avatar})

    try:  # 로그인
        user = USERS.objects.get(username=email)
        user_ser = UserSerializer(user)
        token = Token.objects.get_or_create(user=user)

        return Response(
            data={"token": token[0].key, "user": user_ser.data},
            status=status.HTTP_200_OK,
        )

    except USERS.DoesNotExist:  # 회원가입
        user = USERS.objects.create_user(username=email, first_name=name)
        user_ser = UserSerializer(user)
        token = Token.objects.get_or_create(user=user)

        profile = Profile.objects.get(user=user)
        profile.avatar.save(
            avatar, ContentFile(avatar_response.content), save=True
        )  # Bytes

        return Response(
            data={"token": token[0].key, "user": user_ser.data},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def kakao_login(request):
    ##Code Request##
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    return redirect(url)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def kakao_callback(request):
    ##Access Token Request##
    code = request.query_params["code"]  # 인가 코드
    url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}"
    codeResponse = requests.post(url)
    tokenJson = codeResponse.json()

    profileUrl = "https://kapi.kakao.com/v2/user/me"  # 유저 정보 조회하는 uri
    auth = "Bearer " + tokenJson["access_token"]

    # return Response(data=tokenJson["access_token"])
    headers = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    ##Profile Request##
    response = requests.get(profileUrl, headers=headers)
    profile_json = response.json()
    kakao_account = profile_json.get("kakao_account")

    if not kakao_account["has_email"]:  # false
        return Response(data={"error": "서비스를 이용하기 위해서는 이메일 동의가 필요합니다."})

    email = kakao_account["email"]
    name = kakao_account["profile"]["nickname"]

    avatar_url = kakao_account["profile"]["profile_image_url"]  # url
    avatar = urlparse(avatar_url).path.split("/")[-1]  # url에서 이미지 추출
    avatar_response = requests.get(avatar_url)

    try:  # 로그인
        user = USERS.objects.get(username=email)
        user_ser = UserSerializer(user)
        token = Token.objects.get_or_create(user=user)

        return Response(
            data={"token": token[0].key, "user": user_ser.data},
            status=status.HTTP_200_OK,
        )

    except USERS.DoesNotExist:  # 회원가입
        user = USERS.objects.create_user(username=email, first_name=name)
        user_ser = UserSerializer(user)
        token = Token.objects.get_or_create(user=user)

        profile = Profile.objects.get(user=user)
        profile.avatar.save(
            avatar, ContentFile(avatar_response.content), save=True
        )  # Bytes

        return Response(
            data={"token": token[0].key, "user": user_ser.data},
            status=status.HTTP_200_OK,
        )


# test
@api_view(["GET"])
def kakao_logout(request):
    url = "http://kapi.kakao.com/v1/user/logout"
    access_token = "fRSp1fv-8bJlTJ_zf_qAwvWGXvc3FrPjri7DpQopcSEAAAF_HJwmIw"
    auth = "Bearer " + access_token
    headers = {
        "Authorization": auth,
    }
    requests.post(url, headers=headers)
    return Response(status=200)


##마이페이지 - 프로필##
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def mypage_profile(request):
    if request.method == "GET":  # 조회
        profile = request.user
        serializer = UserSerializer(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":  # 수정
        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)  # 성공
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
