"""restregistration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop_api import views
from example_api import views as v

api_urlpatterns = [
    path('accounts/', include('registration_api.urls')),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('api-auth/', include('rest_framework.urls')),
    path('users/', include('user_api.urls')),
    path('shops/', include('shop_api.urls')),
    path('category-list/', views.AddCategory.as_view(), name = 'category-list'),
    path('category-detail/<int:pk>/', views.CategoryDetail.as_view(), name = 'category-detail'),
    path('product-list/', views.ProductList.as_view(), name = 'product-list'),
    path('ex/', include('example_api.urls')),
    path('cart/', include('cartapi.urls')),
]
