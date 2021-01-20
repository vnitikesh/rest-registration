from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserListSerializer, UserDetailSerializer

# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
