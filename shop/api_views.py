
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
 
from shop.serializers import  CartCreateSerializer, CartItemCreateSerializer, CartPaySerializer, CartSerializer, ProductCreateSerializer, ProfileCreateSerializer, ShopCreateSerializer, UserSerializer, UserSerializerLogin, UserSerializerLoginResponse, UserSerializerRegisterResponse


# @APIView(["POST"])
# def Register_Users(request):
#     try:
#         data = []
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save()
#             account.is_active = True
#             account.save()
#             data["message"] = "user registered successfully"
#             data["email"] = account.email
#             data["username"] = account.username

#         else:
#             data = serializer.errors


#         return Response(data)
#     except IntegrityError as e:
#         account=CustomUser.objects.get(username='')
#         account.delete()
#         raise ValidationError({"400": f'{str(e)}'})

#     except KeyError as e:
#         print(e)
#         raise ValidationError({"400": f'Field {str(e)} missing'})

@swagger_auto_schema(responses={201:UserSerializerRegisterResponse})
class CreateUserView(CreateAPIView):
    model = CustomUser
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={201:UserSerializerRegisterResponse})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
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
        serializer.save(user_type="Buyer")



# class LoginTokenObtainPairSerializer(TokenObtainSerializer):
#     @classmethod
#     def get_token(cls, user):
#         return RefreshToken.for_user(user)

#     def validate(self, attrs):
#         if attrs['user_type'] != 'Seller':
#             return Response({"message":"user is not seller"}, status=status.HTTP_400_BAD_REQUEST)
#         data = super().validate(attrs)
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field],
#             'password': attrs['password'],
#         }

#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['message'] = "user loged in successfully"

#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)

#         return data


# class LoginUserView(TokenViewBase):
#     serializer_class = LoginTokenObtainPairSerializer




class LoginUserView(GenericAPIView):

    serializer_class = UserSerializerLogin
    @swagger_auto_schema(responses={200:UserSerializerLoginResponse})
    def post(self,request):

        try:
            username = request.data['username']
            password = request.data['password']
            
            
            user = CustomUser.objects.get(username=username)
            if not check_password(password,user.password):
                res = {
                    'error': 'password is not true'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            print(user.user_type)
            if user and user.user_type == "Buyer":
                try:
                    refresh = TokenObtainPairSerializer.get_token(user)
                    user_details = {}
                    user_details['refresh'] = str(refresh)
                    user_details['access'] = str(refresh.access_token)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            elif user.user_type != "Buyer":
                res = {
                    'error': 'user in not Buyer'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)
        except CustomUser.DoesNotExist:
            res = {'error': 'user does not exist'}
            return Response(res)



class profile(RetrieveUpdateAPIView,CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        self.kwargs["pk"]=1
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
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.filter(status="Published")
    filterset_class = StoreListFilter
    serializer_class = ShopCreateSerializer

class storecategory(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StoreCategory.objects.all()
    serializer_class = ShopCreateSerializer

class storeproduct(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Product.objects.filter(shop__pk=self.kwargs["id"],shop__deleted=False)
    serializer_class = ProductCreateSerializer
    filterset_class = StoreProductListFilter
    
class createcart(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemCreateSerializer

    @swagger_auto_schema(responses={201:CartPaySerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        if not Cart.objects.filter(user=self.request.user,is_paid=False):
            cart1 = CartCreateSerializer(data=request.data)
            cart1.is_valid(raise_exception=True)
            cart2 = cart1.save(user=request.user)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(cart = cart2,quantity=1)
            headers = self.get_success_headers(serializer.data)
            return Response({'CartId':cart2.id}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            livecart = Cart.objects.get(user=self.request.user,is_paid=False)
            return Response({"message":"just can have on live cart per user","LiveCartId":livecart.id})

        

class addtocart(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemCreateSerializer
    
    def create(self, request, *args, **kwargs):
        livecart = Cart.objects.get(user=self.request.user,is_paid=False)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemCreateSerializer
    
    def create(self, request, *args, **kwargs):
        livecart = Cart.objects.get(user=self.request.user,is_paid=False)
        if CartItem.objects.filter(cart=livecart,product=request.data['product']):
            item = CartItem.objects.get(cart=livecart,product=request.data['product'])
            item.quantity -= 1
            item.save()
            if CartItem.objects.filter(cart=livecart):
                headers = self.get_success_headers({'CartId':livecart.id})
                return Response({'CartId':livecart.id}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                livecart.delete()
                return Response({'message':'live cart deleted because it was empty'})
                
        else:
            return Response({'ERROR':'no such product to delete'})

class paycart(GenericAPIView):

    
    def post(self,request):
        if Cart.objects.filter(user=self.request.user,is_paid=False):
            livecart=Cart.objects.get(user=self.request.user,is_paid=False)
            livecart.is_paid=True
            livecart.save()
            return Response({'message':'Cart has paid successfully'})
        else:
            return Response({'message':'There is no livecart'})


class paidcart(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,is_paid=True)
    serializer_class = CartSerializer


        







    