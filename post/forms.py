from django import forms
from django.contrib.auth.models import User
from django.forms import fields

from post.models import Category, Comment, Post, Tag


class UserFormModel(forms.ModelForm):
    class Meta : 
        model = User
        fields = ['username','email','password']

class Signin(forms.Form):
    username = forms.CharField(max_length=255,min_length=5)
    password =  forms.CharField(widget=forms.PasswordInput)

class PostModelForm(forms.ModelForm):

    class Meta : 
        model = Post
        fields = ['name','image','caption','category','tag','slug']


class PostModelFormView(forms.ModelForm):

    class Meta : 
        model = Post
        fields = "__all__"

class PostDeleteModelForm(forms.ModelForm):
    class Meta : 
        model = Post
        fields = []

class CategoryModelFormView(forms.ModelForm):

    class Meta : 
        model = Category
        fields = "__all__"

class CategoryDeleteModelForm(forms.ModelForm):
    class Meta : 
        model = Category
        fields = []
        
class CommentModelForm(forms.ModelForm):

    class Meta : 
        model = Comment
        fields = ['name','content']

class CommentModelFormView(forms.ModelForm):

    class Meta : 
        model = Comment
        fields = "__all__"

class TagModelFormView(forms.ModelForm):

    class Meta : 
        model = Tag
        fields = "__all__"

class TagDeleteModelForm(forms.ModelForm):
    class Meta : 
        model = Tag
        fields = []