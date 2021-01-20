from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from .models import RegistrationProfile
from rest_framework import serializers
from django.conf import settings


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, label = "Email Address")
    password = serializers.CharField(required = True, label = "Password", style = {'input_type':'password'})
    password_2 = serializers.CharField(required = True, label = "Confirm Password", style = {'input_type':'password'})
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)

    class Meta:
        model = User
        fields = [
        'username', 'email', 'password', 'password_2', 'first_name', 'last_name'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,

            }
        }

    def validate_email(self, value):
        if(User.objects.filter(email = value).exists()):
            raise serializers.ValidationError("Email Already Exists")
        return value

    def validate_password(self, value):
        if(len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8) and len(value) > getattr(settings, 'PASSWORD_MAX_LENGTH', 127)):
            raise serializers.ValidationError("Password should be atleast %s characters long." %getattr(settings, 'PASSWORD_MIN_LENGTH', 8))
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get("password")
        if(password != value):
            raise serializers.ValidationError("Password doesn't match")
        return value

    def validate_username(self, value):
        if(User.objects.filter(username = value).exists()):
            raise serializers.ValidationError("Username already exists")
        return value


    def create(self, validated_data):
        user_data = {
        'username': validated_data.get('username'),
        'email': validated_data.get('email'),
        'password': validated_data.get('password'),
        'first_name': validated_data.get('first_name'),
        'last_name': validated_data.get('last_name')
        }

        user = RegistrationProfile.objects.create_user_profile(
        data = user_data,
        is_active = False,
        site = get_current_site(self.context['request']),
        send_email = True
        )


        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = RegistrationProfile
        fields = [
        'user', 'has_email_verified'
        ]
