from django.shortcuts import render
from .models import Category, Product, Cart, Checkout
from .serializers import CategorySerializer, ProductSerializer, CategoryDetailSerializer, CartSerializer, CheckoutSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class ProductRecordView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    serializer_class = ProductSerializer

    def list(self, request):
        queryset = self.get_queryset()

        serializer_context = {
        'request': request,
        }
        serializer = ProductSerializer(queryset, many = True, context = serializer_context)
        return Response(serializer.data)

'''
    def post(self, request):
        serializer_context = {
        'request': request,
        }
        print(request.data)
        serializer = ProductSerializer(data = request.data, context = serializer_context)
        if(serializer.is_valid(raise_exception = ValueError)):
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status.HTTP_400_BAD_REQUEST)
'''
class CartViewSet(generics.ListCreateAPIView):
    def get_queryset(self):
        cart = Cart.objects.filter(user = self.request.user)[::-1]
        return cart

    serializer_class = CartSerializer

class CheckoutView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Checkout.objects.filter(user = self.request.user).last()
        return queryset
    serializer_class = CheckoutSerializer
    def list(self, request):
        checkout = self.get_queryset()

        #print(checkout.delivery_address)
        serializer = CheckoutSerializer(checkout)
        return Response(serializer.data)

    def merge_dict(self, dict1, dict2):
        return dict2.update(dict1)

    def send_confirmation_email(self, dict):
        context = {
        'user': self.request.user,
        'dict': dict,


        }
        subject = render_to_string('confirmation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('confirmation_email_content.txt',context)

        msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [self.request.user.email])
        msg.attach_alternative(message, "text/html")
        msg.send()

    def create(self, request, format = None):
        cart = Cart.objects.filter(user = self.request.user)
        total_cost_count = 0
        cart_list = {}
        for i in cart:
            total_cost_count += i.subtotal
            if(i.items_ordered in cart_list):
                cart_list[i.items_ordered] += i.subtotal
            else:
                cart_list[i.items_ordered] = i.subtotal




        if(str(total_cost_count) == request.data['item_total_cost']):
            print(type(request.data))
            print(type(cart_list))
            self.merge_dict(cart_list, request.data)
            serializer = CheckoutSerializer(data = request.data)
            if(serializer.is_valid(raise_exception = ValueError)):
                serializer.create(validated_data = request.data, user = self.request.user)
                lst = []

                dict = {}
                for i in cart:
                    if(i.shop.shop_name not in dict):
                        dict['shop_name'] = i.shop.shop_name
                        lst.append(i.shop.shop_name)

                    dict[i.items_ordered] = [i.subtotal,i.quantities]
                    lst.append(i.subtotal)
                    lst.append(i.items_ordered)
                    lst.append(i.quantities)
                print(lst)
                self.send_confirmation_email(dict)
                cart.delete()
                return Response(serializer.data, status = status.HTTP_201_CREATED)

            return Response(serializer.error_messages, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data":"Something fishy has been done on client side"})





'''
class CategoryDetailView(APIView):
    def get_prod_object(self, pk):
        try:
            category = Category.objects.get(pk = pk)
            product = Product.objects.filter(category = category)
            #print(product.name)
            return Product.objects.filter(category = Category.objects.get(pk = pk))
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        product = self.get_prod_object(pk)
        print(product)
        serializer = CategoryDetailSerializer(product, many = True)
        return Response(serializer.data)

    def get_category_object(self, pk):
        category = Category.objects.get(pk = pk)
        return category

    def post(self, request, pk, format = None):
        cat = self.get_category_object(pk)
        serializer = CategoryDetailSerializer(cat, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
'''
