from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from django.contrib.auth import authenticate, get_user_model
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils.translation import gettext_lazy as _
import base64
import binascii

from rest_framework.permissions import BasePermission

# class BuyerAuthentication(authentication.BaseAuthentication):

#     def authenticate_credentials(self, userid, password, request=None):
#         """
#         Authenticate the userid and password against username and password
#         with optional request for context.
#         """
#         credentials = {
#             get_user_model().USERNAME_FIELD: userid,
#             'password': password
#         }
#         user = authenticate(request=request, **credentials)

#         if user is None:
#             raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

#         if user.user_type != "Buyer":
#             raise exceptions.AuthenticationFailed(_('User is not buyer'))

#         if not user.is_active:
#             raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

#         return (user, None)

    
class BuyerPermission(BasePermission):

    def has_permission(self, request, view):

        if request.user.user_type == "Buyer":
            return True
        else:
            return False 