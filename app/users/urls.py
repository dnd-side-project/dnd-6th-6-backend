from django.urls import path, include
from users.views import (
    UserViewSet,
    auth_email,
    auth_code,
    password,
    login_email,
    login_password,
    logout,
    profile,
    kakao_login,
    kakao_callback,
    naver_login,
    naver_callback,
    mypage_profile,
)

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

urlpatterns = [
    path("", user_list),
    path("<int:pk>", user_detail),
    path("email", auth_email),
    path("code", auth_code),
    path("password", password),
    path("profile", profile),
    path("login/email", login_email),
    path("login/password", login_password),
    path("logout", logout),
    path("login/kakao", kakao_login),
    path("login/kakao/callback", kakao_callback),
    path("login/naver", naver_login),
    path("login/naver/callback", naver_callback),
    path("mypage/profile", mypage_profile),
]
