from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSignupSerializer(serializers.Serializer):
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]*$',
        message='Username must contain only letters, numbers, and underscores.'
    )

    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username = serializers.CharField(validators=[username_validator])
    password=serializers.CharField()

    def validate_password(self, data):
        try:
            validate_password(data)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return data

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists() :
            raise serializers.ValidationError("Username already exists")
        return data
    
    def create(self, validated_data):
        user=User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
        }
        return token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Enter valid Username and Password")
        return data
   
    def get_tokens_for_user(self,data):
        username = data['username']
        password = data['password']
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                token= {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username':username,
                }
                return token


class PasswordChangeSerializer(serializers.Serializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField()
    confirm_password=serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"message": "Both New passwords and Confirm Password must match."})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"message": "New passwords must be different than Old Password."})
        return data
    
    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    
    def save(self, user):
        if user.is_anonymous:
            raise serializers.ValidationError("Anonymous users cannot change passwords.")
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError("Old password is not correct.")
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user