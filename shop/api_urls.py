from django.urls import path

from shop.api_views import CreateUserView, LoginUserView, addtocart, createcart, deletecartitem, paidcart, paycart, profile, store, storecategory, storeproduct


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='api-register'),
    path('login/', LoginUserView.as_view(), name='api-login'),
    path('profile/', profile.as_view(), name='profile'),
    path('store/', store.as_view(), name='store'),
    path('store/category/', storecategory.as_view(), name='storecategory'),
    path('store/<int:id>/product/', storeproduct.as_view(), name='storeproduct'),
    path('cart/createcart/', createcart.as_view(),name='createcart'),
    path('cart/addtocart/', addtocart.as_view(),name='addtocart'),
    path('cart/deletecartitem/', deletecartitem.as_view(),name='deletecartitem'),
    path('cart/paycart/', paycart.as_view(),name='paycart'),
    path('cart/paidcarts/', paidcart.as_view(),name='paidcarts'),



    
]
