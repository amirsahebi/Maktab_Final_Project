from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache
UserModel = get_user_model()


class PhoneSellerBackend(ModelBackend):

    def authenticate(self, request, username, password):
        try:
            # login with phone and token
            user = UserModel.objects.get(phone=username)
            if user:
                if not check_password(password,user.password):
                    return None
                if user.user_type == "Seller":
                    return user
                else:
                    return None
        except UserModel.DoesNotExist:
            return None 
 

class PhoneBuyerBackend(ModelBackend):

    def authenticate(self, request, username, password):
        try:
            # login with phone and token
            user = UserModel.objects.get(phone=username)
            if user:
                if not str(cache.get("totp")) == password and not check_password(password,user.password):
                    return None
                if user.user_type == "Buyer":
                    return user
                else:
                    return None
        except UserModel.DoesNotExist:
            return None 
