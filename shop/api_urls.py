from django.urls import path

from shop.api_views import CreateUserView, LoginUserView


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    
]
