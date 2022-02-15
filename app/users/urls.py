from django.urls import path, include
from users.views import (
    UserViewSet,
    EmailAuthSet,
    password,
    code,
    login,
    logout,
    profile,
    test,
    kakao_login,
    kakao_callback,
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
    path("login/", login),
    path("logout/", logout),
    path("login/kakao/", kakao_login),
    path("login/kakao/callback/", kakao_callback),
    path("accounts/", include("allauth.urls")),
    # path("login/", obtain_auth_token),
    path("test/", test),  # test
]
