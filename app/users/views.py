from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response


# Generic CBV 사용
# 모든 유저
class UserList(generics.ListCreateAPIView):  # get, post
    users = get_user_model()
    queryset = users.objects.all()
    serializer_class = UserSerializer


# 해당 유저
class UserDetail(generics.ListCreateAPIView):
    # queryset = Profile.objects.all()
    # serializer_class = ProfileSerializer
    pass
