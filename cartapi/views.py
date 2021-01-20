from django.shortcuts import render
from .serializers import ProductSerializer
from .models import Product
from rest_framework import generics

# Create your views here.

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
