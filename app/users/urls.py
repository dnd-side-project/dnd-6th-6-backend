from django.urls import path
from users.views import UserViewSet, EmailAuthSet

user_list = UserViewSet.as_view(
    {
        "get": "list",  # 유저 목록
        "post": "create",  # 회원가입
    }
)

user_detail = UserViewSet.as_view(
    {
        "get": "retrieve",  # 해당 유저 조회
        "put": "update",  # 수정
    }
)

email_list = EmailAuthSet.as_view(
    {
        "get": "list",  # 유저 목록
        "post": "create",
    }
)


urlpatterns = [
    path("", user_list),
    path("<int:pk>/", user_detail),
    path("signup/", email_list),
]
