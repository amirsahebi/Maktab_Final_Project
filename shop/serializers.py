from dataclasses import fields
from email import message
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


class ShopCreateSerializer(serializers.ModelSerializer):
    

    class Meta : 
        model = Store
        fields = ['name','image','type']

class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Product
        fields = ['name','image','caption','category','tag','slug','cost','available_count']

class CartCreateSerializer(serializers.ModelSerializer):
    

    class Meta : 
        model = Cart
        fields = []

class CartItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["product"]

class ProfileCreateSerializer(serializers.ModelSerializer):
    

    class Meta: 
        model = Profile
        fields = ['name','image']

class CartPaySerializer(serializers.ModelSerializer):


    class Meta: 
        model = Cart
        fields = ['pk']

class CartSerializer(serializers.ModelSerializer):



    class Meta: 
        model = Cart
        fields = ['pk','created_at']

class UserSerializerRegisterResponse(serializers.ModelSerializer):
    message = serializers.CharField()


    class Meta:
        model = CustomUser
        fields = ['message']

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)


class PhoneUserSerializer(serializers.ModelSerializer):



    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            phone=validated_data['phone'],
            username=validated_data['phone'],
            token = validated_data['token']
        )
        return user

    class Meta:
        model = CustomUser
        # Tuple of serialized model fields (see link [2])
        fields = ['phone','token']