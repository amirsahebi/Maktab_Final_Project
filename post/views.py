from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Category, Comment, Post, Tag
from .forms import CategoryDeleteModelForm, CategoryModelFormView, CommentModelForm, CommentModelFormView, PostDeleteModelForm, PostModelForm, PostModelFormView, Signin, TagModelFormView, UserFormModel


# class PostListView(View):
#     form_class = Post
#     template_name = 'post_list.html'

#     @login_required(login_url='/login/')
#     def get(self, request, *args, **kwargs):
#         posts = self.form_class.objects.filter(owner=request.user)
#         return render(request, self.template_name, {'posts': posts})

@login_required(login_url='/login/')
def PostListView(request):
    posts = Post.objects.filter(owner=request.user)
    return render(request, 'post_list.html', {'posts': posts})


class PostDetailView(View):
    model = Post
    template_name = 'post_detail.html'
    
    def get(self, request, *args, **kwargs):
        form = CommentModelForm()
        self.post = self.model.objects.get(slug=self.kwargs['slug'])
        return render(request, 'post_detail.html',{'post':self.post,'form':form})
    
    def post(self, request, *args, **kwargs):
        updated_request = request.POST.copy()
        updated_request.update({'post': self.model.objects.get(slug=self.kwargs['slug'])})
        form = CommentModelFormView(updated_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment successfully saved!')
            return HttpResponseRedirect(self.request.path_info)


def CategoryListView(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html',{'categories':categories})

def CategoryDetailView(request,slug):
    category = Category.objects.filter(slug=slug)[0]
    return render(request,'category_detail.html',{'category':category})

def TagListView(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html',{'tags':tags})

def TagDetailView(request,id):
    tag = Tag.objects.get(id=id)
    return render(request,'tag_detail.html',{'tag':tag})

from django.contrib.auth.models import User
def myRegister(request):
    form = UserFormModel(None or request.POST)
    if request.method == "POST":
        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
            return redirect(reverse('post_list'))
    
    return render(request,'forms/register.html',{'form':form})


def login_user(request):
    form = Signin()
    if request.method == "POST":
        form = Signin(request.POST)
        if form.is_valid():
            print(form)
            user = authenticate(username= form.cleaned_data['username'],password= form.cleaned_data['password'])
            if user is not None :
                print("logged in")
                login(request,user)
                next = request.GET.get('next')
                if next : 
                    return redirect(request.GET.get('next')) 
                return redirect(reverse('post_list')) 

    return render(request,'forms/login.html' ,{'form':form})


@login_required(login_url='/login/')
def AddPost(request):
    form = PostModelForm()
    if request.method == "POST":
        form = PostModelForm(request.POST,request.FILES)
        if form.is_valid():
            updated_request = request.POST.copy()
            updated_request.update({'owner': f'{request.user.id}'})
            form = PostModelFormView(updated_request,request.FILES)
            form.save()
            messages.add_message(request, messages.ERROR, f'The post successfully saved!',extra_tags="success")
            return redirect(reverse('post_list'))

    return render(request,'forms/post_form.html',{'form':form})

@login_required(login_url='/login/')
def EditPost(request,slug):
    post = get_object_or_404(Post,slug=slug)
    if post.owner.id == request.user.id:
        form = PostModelForm(instance=post)

        if request.method == "POST":
            form =PostModelForm(request.POST,instance=post) 
            if form.is_valid():
                form.save()
                return redirect(reverse('post_list'))

        return render(request,'forms/edit_post_form.html',{'form':form,'post':post})

    else:
        raise PermissionDenied()

@login_required(login_url='/login/')
def DeletePost(request,slug):
    
    post = get_object_or_404(Post,slug=slug)
    
    form = PostDeleteModelForm(instance=post)
    if request.method == "POST":
        post.delete()
        return redirect('/') 


    return render(request,'forms/delete_post_form.html',{'form':form,'post':post})
    


def EditCategory(request,slug):
    category = get_object_or_404(Category,slug=slug)
    form = CategoryModelFormView(instance=category)

    if request.method == "POST":
        form =CategoryModelFormView(request.POST,instance=category) 
        if form.is_valid():
            form.save()
            return redirect(reverse('category_list'))

    return render(request,'forms/edit_category_form.html',{'form':form,'category':category})

    

def DeleteCategory(request,slug):
    
    category = get_object_or_404(Category,slug=slug)
    
    form = CategoryDeleteModelForm(instance=category)
    if request.method == "POST":
        category.delete()
        return redirect(reverse('category_list')) 

    return render(request,'forms/delete_category_form.html',{'form':form,'category':category})


def AddCategory(request):
    form = CategoryModelFormView()
    if request.method == "POST":
        form = CategoryModelFormView(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.ERROR, f'The category successfully saved!',extra_tags="success")
            return redirect(reverse('category_list'))

    return render(request,'forms/category_form.html',{'form':form})


def AddComment(request):
    form = CommentModelFormView()
    if request.method == "POST":
        form = CommentModelFormView(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.ERROR, f'The post successfully saved!',extra_tags="success")
            return redirect(reverse('category_list'))

    return render(request,'forms/category_form.html',{'form':form})


class SearchResultsView(ListView):
    model = Post
    template_name = 'forms/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Post.objects.filter(
                Q(name__icontains=query) | Q(caption__icontains=query)
            )
        else:
            object_list = None
        return object_list

def EditTag(request,id):
    tag = get_object_or_404(Tag,id=id)
    form = TagModelFormView(instance=tag)

    if request.method == "POST":
        form =TagModelFormView(request.POST,instance=tag) 
        if form.is_valid():
            form.save()
            return redirect(reverse('tag_list'))

    return render(request,'forms/edit_tag_form.html',{'form':form,'tag':tag})

    
def DeleteTag(request,id):
    
    tag = get_object_or_404(Tag,id=id)
    
    form = CategoryDeleteModelForm(instance=tag)
    if request.method == "POST":
        tag.delete()
        return redirect(reverse('tag_list')) 

    return render(request,'forms/delete_tag.html',{'form':form,'tag':tag})

def AddTag(request):
    form = TagModelFormView()
    if request.method == "POST":
        form = TagModelFormView(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.ERROR, f'The post successfully saved!',extra_tags="success")
            return redirect(reverse('tag_list'))

    return render(request,'forms/tag_form.html',{'form':form})
