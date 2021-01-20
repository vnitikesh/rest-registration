from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, views
from .serializers import *
from rest_framework.response import Response
# Create your views here.
User = get_user_model()

class UserRegisrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class UserEmailVerificationAPIView(views.APIView):
    def get(self, request, verification_key):
        activated_user = self.activate(verification_key)
        if(activated_user):
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_204_NO_CONTENT)

    def activate(self, verification_key):
        return RegistrationProfile.objects.activate_user(verification_key)
