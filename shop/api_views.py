from itertools import product
import random
import pyotp
from django.core.cache import cache
from rest_pyotp.views import PyotpViewset
from django.http import response
from django.urls import reverse
from rest_framework.views import APIView
from DrfMaktab import settings
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.views import TokenViewBase
from shop.authentication import BuyerPermission
from shop.filter import StoreListFilter, StoreProductListFilter
from shop.models import Cart, CartItem, CustomUser, Product, Profile, Store, StoreCategory
from rest_framework import status
from rest_framework_simplejwt.serializers import RefreshToken, SlidingToken, TokenObtainSerializer, UntypedToken,TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from django.contrib.auth.signals import user_logged_in
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.hashers import make_password , check_password
from drf_yasg.utils import swagger_auto_schema
import requests
 
from shop.serializers import  CartCreateSerializer, CartItemCreateSerializer, CartPaySerializer, CartSerializer, PhoneSerializer, PhoneUserSerializer, ProductCreateSerializer, ProfileCreateSerializer, ShopCreateSerializer, UserSerializer, UserSerializerLogin, UserSerializerLoginResponse, UserSerializerRegisterResponse




class CreateUserView(CreateAPIView):
    model = CustomUser
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={201:UserSerializerRegisterResponse})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        #TODO
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            user.user_type="Buyer"
            user.save()
            headers = self.get_success_headers(serializer.data)
            return Response({"message":"user registered successfully"}, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            account=CustomUser.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})

    def perform_create(self, serializer):
        return serializer.save()



class profile(RetrieveUpdateAPIView,CreateAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    def get_queryset(self):
        self.kwargs["pk"]=(Profile.objects.filter(owner=self.request.user)[0]).pk
        return Profile.objects.filter(owner=self.request.user)
    serializer_class = ProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        if not Profile.objects.filter(owner=self.request.user):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"message":"just can have one profile per user"})


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class store(ListAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    queryset = Store.objects.filter(status="Published")
    filterset_class = StoreListFilter
    serializer_class = ShopCreateSerializer

class storecategory(ListAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    queryset = StoreCategory.objects.all()
    serializer_class = ShopCreateSerializer

class storeproduct(ListAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    def get_queryset(self):
        return Product.objects.filter(shop__pk=self.kwargs["id"],shop__deleted=False)
    serializer_class = ProductCreateSerializer
    filterset_class = StoreProductListFilter
    
class createcart(CreateAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    serializer_class = CartItemCreateSerializer

    @swagger_auto_schema(responses={201:CartPaySerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        thisproduct = Product.objects.get(pk=self.request.data['product'])
        if not Cart.objects.filter(shop=thisproduct.shop,user=self.request.user,is_paid=False):
            cart1 = CartCreateSerializer(data=request.data)
            cart1.is_valid(raise_exception=True)
            cart2 = cart1.save(user=request.user,shop=thisproduct.shop)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(cart = cart2,quantity=1)
            headers = self.get_success_headers(serializer.data)
            return Response({'CartId':cart2.id}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            livecart = Cart.objects.get(user=self.request.user,is_paid=False)
            return Response({"message":"just can have one live cart per user for each shop","LiveCartId":livecart.id})

        

class addtocart(CreateAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    serializer_class = CartItemCreateSerializer
    
    def create(self, request, *args, **kwargs):
        thisproduct = Product.objects.get(pk=self.request.data['product'])
        livecart = Cart.objects.filter(shop=thisproduct.shop,user=self.request.user,is_paid=False)
        if livecart[0]:
            livecart=livecart[0]
        else:
            Response({"Error":"There is no live cart for this user in this shop"})
        if CartItem.objects.filter(cart=livecart,product=request.data['product']):
            item = CartItem.objects.get(cart=livecart,product=request.data['product'])
            item.quantity += 1
            item.save()
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(cart = livecart,quantity=1)
        headers = self.get_success_headers({'CartId':livecart.id})
        return Response({'CartId':livecart.id}, status=status.HTTP_201_CREATED, headers=headers)


class deletecartitem(CreateAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission)
    serializer_class = CartItemCreateSerializer
    
    def create(self, request, *args, **kwargs):
        thisproduct = Product.objects.get(pk=self.request.data['product'])
        livecart = Cart.objects.get(shop=thisproduct.shop,user=self.request.user,is_paid=False)
        if CartItem.objects.filter(cart=livecart,product=request.data['product']):
            item = CartItem.objects.get(cart=livecart,product=request.data['product'])
            item.quantity -= 1
            item.save()
            if CartItem.objects.filter(cart=livecart):
                headers = self.get_success_headers({'CartId':livecart.id})
                return Response({'CartId':livecart.id}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                livecart.delete()
                return Response({'message':'live cart deleted because it was empty'},status=status.HTTP_200_OK)
                
        else:
            return Response({'ERROR':'no such product to delete'},status=status.HTTP_401_UNAUTHORIZED)

class paycart(GenericAPIView):

    permission_classes = (IsAuthenticated,BuyerPermission,)

    
    def post(self,request):
        if Cart.objects.filter(user=self.request.user,is_paid=False):
            livecarts=Cart.objects.filter(user=self.request.user,is_paid=False)
            for livecart in livecarts:
                livecart.is_paid=True
                livecart.save()
                for cartitem in CartItem.objects.filter(cart=livecart):
                    product = Product.objects.get(pk=cartitem.product.id)
                    product.available_count -= cartitem.quantity
                    product.save()
                return Response({'message':'Cart has paid successfully'})
        else:
            return Response({'message':'There is no livecart'},status=status.HTTP_401_UNAUTHORIZED)


class paidcart(ListAPIView):
    permission_classes = (IsAuthenticated,BuyerPermission,)
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,is_paid=True)
    serializer_class = CartSerializer


class Otp():
    def generate_totp():
        
        otp = random.randint(100000, 999999)

        return otp


class sendcode(GenericAPIView):

    serializer_class = PhoneSerializer

    def post(self,request):
        phone = PhoneSerializer(request.data)
        totp = Otp.generate_totp()
        cache.set('totp',{'totp':totp,'phone':phone.data["phone"]},300)
        body = {'receptor':phone.data["phone"],'token':totp,'template':"verify"}
        # sms_res = requests.get("https://api.kavenegar.com/v1/73577961477A66706C7A304A634E4D4145646C5437795A375833674E5A67754478416276584462787374413D/verify/lookup.json",params=body)
        # if sms_res.json()['return']['status']==200:
        #     return Response(sms_res.json())
        # else:
        #     return Response(sms_res.json(),status=status.HTTP_401_UNAUTHORIZED)
        return Response(body,status=status.HTTP_200_OK)
    

class CreatePhoneUserView(CreateAPIView):
    model = CustomUser
    serializer_class = PhoneUserSerializer

    @swagger_auto_schema(responses={201:UserSerializerRegisterResponse})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['token'] == cache.get("totp")['totp'] and serializer.validated_data['phone'] == cache.get("totp")['phone']:
            if not CustomUser.objects.filter(phone=serializer.validated_data['phone']):
                user = self.perform_create(serializer)
                user.user_type="Buyer"
                user.save()
                headers = self.get_success_headers(serializer.data)
                return Response({"message":"user registered successfully"}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                headers = self.get_success_headers(serializer.data)
                return Response({"message":"A user has registered with this phone number!"}, status=status.HTTP_401_UNAUTHORIZED, headers=headers)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response({"message":"token is wrong or expired!"}, status=status.HTTP_401_UNAUTHORIZED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()








    