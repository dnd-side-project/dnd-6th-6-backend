from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


# Generic CBV 사용
# 모든 유저
class UserListAPIView(APIView):  # get, post
    users = get_user_model()

    def get(self, request):
        serializer = UserSerializer(self.users.objects.all(), many=True)
        return Response(serializer.data)


# 해당 유저 정보
class UserDetailAPIView(APIView):
    users = get_user_model()

    def get_object(self, pk):
        return get_object_or_404(self.users, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = UserSerializer(post)
        return Response(serializer.data)
