from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("profile/", views.UserList.as_view()),
    path("profile/<int:pk>", views.UserDetail.as_view()),
]
