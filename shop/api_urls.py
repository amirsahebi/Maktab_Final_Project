from django.urls import path, include

from shop.api_views import CreatePhoneUserView, CreateUserView,addtocart, createcart, deletecartitem, sendcode, paidcart, paycart, profile, store, storecategory, storeproduct
import rest_pyotp

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='api-register'),
    path('profile/', profile.as_view(), name='profile'),
    path('store/', store.as_view(), name='store'),
    path('store/category/', storecategory.as_view(), name='storecategory'),
    path('store/<int:id>/product/', storeproduct.as_view(), name='storeproduct'),
    path('cart/createcart/', createcart.as_view(),name='createcart'),
    path('cart/addtocart/', addtocart.as_view(),name='addtocart'),
    path('cart/deletecartitem/', deletecartitem.as_view(),name='deletecartitem'),
    path('cart/paycart/', paycart.as_view(),name='paycart'),
    path('cart/paidcarts/', paidcart.as_view(),name='paidcarts'),
    path('sendcode/', sendcode.as_view(),name='sendcode'),
    path('phoneregister/', CreatePhoneUserView.as_view(), name='phone-api-register'),
]
