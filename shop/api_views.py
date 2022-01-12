
from rest_framework.views import APIView
from DrfMaktab import settings
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.views import TokenViewBase
from shop.models import CustomUser
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
 
from shop.serializers import  UserSerializer, UserSerializerLogin, UserSerializerLoginResponse


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


class CreateUserView(CreateAPIView):
    model = CustomUser
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
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



@swagger_auto_schema(responses={'refresh token':'a','access token':'b'})
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
            if user and user.user_type == "Seller":
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
            elif user.user_type != "Seller":
                res = {
                    'error': 'user in not seller'}
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





