from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ShopCreateForm(forms.ModelForm):

    class Meta : 
        model = Store
        fields = ['name','image']

class ProductCreateForm(forms.ModelForm):

    class Meta : 
        model = Product
        fields = ['name','image','caption','category','tag','slug']

class SignUpForm(UserCreationForm):

   class Meta:
      model = CustomUser 
      fields = ['username', 'email', 'password1','password2']