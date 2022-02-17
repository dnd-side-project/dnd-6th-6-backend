from django.urls import path, include
from users.views import (
    UserViewSet,
    EmailAuthSet,
    kakao_callback,
    password,
    code,
    login_email,
    login_password,
    logout,
    profile,
    kakao_login,
    kakao_callback,
    naver_login,
    naver_callback,
    naver_logout,
)

# from rest_framework_simpletwt.views import
# users/
user_list = UserViewSet.as_view(
    {
        "get": "list",  # 유저 목록
        "post": "create",  # 회원가입
    }
)

# users/{user-id}
user_detail = UserViewSet.as_view(
    {
        "get": "retrieve",  # 해당 유저 조회
        "put": "update",  # 수정
    }
)

# users/email
email_list = EmailAuthSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", user_list),
    path("<int:pk>/", user_detail),
    path("email/", email_list),
    path("password/", password),
    path("code/", code),
    path("profile/", profile),
    path("login/email", login_email),
    path("login/password", login_password),
    path("logout/", logout),
    path("login/kakao/", kakao_login),
    path("login/kakao/callback/", kakao_callback),
    path("login/naver/", naver_login),
    path("login/naver/callback/", naver_callback),
    path("logout/naver/", naver_logout),
]
