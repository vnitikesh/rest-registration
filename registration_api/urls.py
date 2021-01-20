from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('register/', views.UserRegisrationAPIView.as_view(), name = 'register'),
    url(r'^verify/(?P<verification_key>.+)/$', views. UserEmailVerificationAPIView.as_view(), name = 'email_verify'),
    #path('activate/', views.activate, name = 'account_activate')
]
