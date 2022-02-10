from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, EmailAuthSerializer
from .models import Profile, EmailAuth

USERS = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = USERS.objects.all()
    serializer_class = UserSerializer


class EmailAuthSet(viewsets.ModelViewSet):  # POST
    queryset = EmailAuth.objects.all()
    serializer_class = EmailAuthSerializer
