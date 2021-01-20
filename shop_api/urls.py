from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopList.as_view(), name = 'shop-list'),
    path('<int:pk>/', views.ShopDetail.as_view(), name = 'shop-detail'),
    
]
