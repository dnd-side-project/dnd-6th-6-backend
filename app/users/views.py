from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .serializers import UserSerializer, ProfileSerializer

USERS = get_user_model()


class UserListAPIView(APIView):  # get, post
    def get(self, request):
        serializer = UserSerializer(USERS.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erreos, status=400)


# 해당 유저 정보
class UserDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(USERS.objects.all(), pk=pk)

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# 프로필
class ProfileListAPIView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():  # 유효성 검사
            serializer.save()
            return Response(serializer.data, stauts=201)
        return Response(serializer.erreos, status=400)
