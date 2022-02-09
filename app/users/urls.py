from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.UserListAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),
    path("profile/", views.ProfileListAPIView.as_view()),
]
