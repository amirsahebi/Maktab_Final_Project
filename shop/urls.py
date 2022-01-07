from django.contrib.auth import login
from django.urls import path
from django.urls.resolvers import URLPattern


from shop.views import login_user, myRegister
from shop.views import CreateShop, Dashboard, DeleteShop, EditShop, CreateProduct, OrderDetail, Orderlist
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(Dashboard.as_view(),login_url='login/'), name='dashboard'),
    path('createshop/', login_required(CreateShop.as_view(),login_url='login/'), name='createshop'),
    path('editshop/',login_required(EditShop.as_view(),login_url='login/'), name='editshop'),
    path('deleteshop/',login_required(DeleteShop.as_view(),login_url='login/'), name='deleteshop'),
    path('createproduct/',login_required(CreateProduct.as_view(),login_url='login/'), name='createproduct'),
    path('orderlist/<int:id>',login_required(OrderDetail.as_view(),login_url='login/'), name='orderdetail'),
    path('orderlist/',login_required(Orderlist.as_view(),login_url='login/'), name='orderlist'),
    path('logout/',login_required(logout,login_url='login/'), name='logout'),
    path('register/', myRegister ,name="register"),
    path('login/', login_user ,name="login"),

]
