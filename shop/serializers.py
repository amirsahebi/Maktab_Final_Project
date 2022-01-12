from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

class UserSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = CustomUser
        # Tuple of serialized model fields (see link [2])
        fields = ['username', 'email', 'password']


class UserSerializerLogin(serializers.ModelSerializer):

    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserSerializerLoginResponse(serializers.ModelSerializer):
    refresh_token= serializers.CharField()
    access_token= serializers.CharField()

    
    class Meta:
        model = CustomUser
        fields = ['refresh_token', 'access_token']




