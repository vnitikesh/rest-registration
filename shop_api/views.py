from django.shortcuts import render
from rest_framework import generics
from .models import Shop, Category, Product
from rest_framework import permissions
from .serializers import ShopSerializer, CategoryListSerializer, CategoryDetailSerializer, ProductSerializer
from .permissions import IsOwnerOrReadOnly, IsShopOrReadOnly
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

class AddCategory(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly
    ]
    name = 'category-list'

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly
    ]

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
    permissions.IsAuthenticatedOrReadOnly
    ]
