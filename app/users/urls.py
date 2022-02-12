from django.urls import path, include
from users.views import UserViewSet, EmailAuthSet, sign_up, auth_code, log_in, profile

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


urlpatterns = [
    path("", user_list),
    path("<int:pk>/", user_detail),
    path("email/", email_list),
    path("signup/", sign_up),
    path("login/", log_in),
    path("auth/", auth_code),
    path("profile/", profile)
    #    path("dj-account/", include("dj_rest_auth.urls")),  # 로그인, 로그아웃
    #    path("dj-signup/", include("dj_rest_auth.registration.urls")),  # 회원가입
    #    path("accounts/", include("allauth.urls")),
    # path("accounts/", include("accounts.urls")),
]
