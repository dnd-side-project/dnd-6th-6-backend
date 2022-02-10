from django.urls import path
from users.views import UserViewSet, EmailAuthSet

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
]
