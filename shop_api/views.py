from django.shortcuts import render
from rest_framework import generics
from .models import Shop
from rest_framework import permissions
from .serializers import ShopSerializer
from example_api.serializers import CategorySerializer
from .permissions import IsOwnerOrReadOnly, IsShopOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class ShopList(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class ShopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]
