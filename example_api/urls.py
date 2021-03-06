from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name = 'category-list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name = 'category-detail'),
    path('product/', views.ProductRecordView.as_view(), name = 'product-list'),
    path('cart/', views.CartViewSet.as_view(), name = 'cart'),
    path('checkout/', views.CheckoutView.as_view(), name = 'checkout'),
    #path('order/', views.OrderViewSet.as_view(), name = 'order')
]
