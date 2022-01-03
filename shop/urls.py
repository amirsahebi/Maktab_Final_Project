from django.contrib.auth import login
from django.urls import path
from django.urls.resolvers import URLPattern

from post.forms import PostModelForm, Signin
from shop.views import Dashboard

urlpatterns = [
    path('',Dashboard.as_view(), name='dashbord'),
    
]
