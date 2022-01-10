from decimal import Decimal
from typing import OrderedDict
from django import views
from django.db.models import F, Sum
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
import datetime

# Create your views here.
from django.views.generic import ListView, DetailView
from post.forms import Signin, UserFormModel
from post.models import Category, Post

from shop.forms import ProductCreateForm, ShopCreateForm, SignUpForm
from .models import Cart, CartItem, CustomUser, Product, Store

# Create your views here.
class Dashboard(View):
    template_name = 'dashboard.html'
    
    def get(self, request, *args, **kwargs):
        if Store.objects.filter(owner__id=request.user.id,deleted=False):
            shop = Store.objects.get(owner__id=request.user.id,deleted=False)
            buyers = CustomUser.objects.filter(user_type="Buyer")
            print(buyers)
            buyers_detail=[]
            for buyer in buyers:
                buyers_detail.append({
                    "name":buyer.name,
                    "last_buy":(Cart.objects.filter(user=buyer,is_paid=True,accepted=True).order_by('-created_at')[0]).created_at,
                    "carts_count":Cart.objects.filter(user=buyer,is_paid=True,accepted=True).count(),
                    "total_cost":CartItem.objects.filter(cart__user=buyer).aggregate(total_price=Sum(F('quantity') * F('product__cost')))['total_price'] or Decimal('0'),
                    "products_count":CartItem.objects.filter(cart__user=buyer).aggregate(total_count=Sum(F('quantity')))['total_count'] or Decimal('0')
                })
            print(buyers_detail)
            orders_date = [0]*7
            orders_count = [0]*7
            for i in range(0,7):
                orders_count[i] += Cart.objects.filter(created_at__range=[(datetime.date.today()-datetime.timedelta(days=i+1)).strftime("%Y-%m-%d"),(datetime.date.today()-datetime.timedelta(days=i)).strftime("%Y-%m-%d")]).count()
                orders_date[i] = int((datetime.date.today()-datetime.timedelta(days=i+1)).strftime("%d"))
        else:
            shop=0
        return render(request, self.template_name , {'shop': shop,'buyers_detail':buyers_detail,'orders_date':orders_date[::-1],'orders_count':orders_count[::-1]})

    def post(self, request, *args, **kwargs):
        form = ShopCreateForm(request.POST, request.FILES)
        if form.is_valid():
            n = form.save()
            n.owner = request.user
            n.save()
            return HttpResponseRedirect(self.request.path_info)


class CreateShop(View):
    
    template_name = 'form/createshop.html'

    def get(self, request, *args, **kwargs):
        form = ShopCreateForm()
        shop = Store.objects.filter(owner__id = request.user.id,deleted = False)
        # function if someone has a shop can't create more
        allow = 0
        if shop :
            allow = 1
        return render(request, self.template_name , {'form': form,'allow':allow})

    def post(self, request, *args, **kwargs):
        form = ShopCreateForm(request.POST, request.FILES)
        if form.is_valid():
            n = form.save(commit=False)
            n.owner = request.user
            n.save()
            return HttpResponseRedirect(self.request.path_info)

class EditShop(View):
    
    template_name = 'form/editshop.html'

    def get(self, request, *args, **kwargs):
        if Store.objects.filter(owner__id=request.user.id,deleted=False):
            shop = Store.objects.filter(owner__id=request.user.id,deleted=False)[0]
            form = ShopCreateForm(instance=shop)
            allow = 0
        else:
            form = ShopCreateForm()
            allow = 1

        return render(request, self.template_name , {'form': form,'allow':allow})

    def post(self, request, *args, **kwargs):
        shop = Store.objects.get(owner=request.user,deleted=False)
        form = ShopCreateForm(request.POST,instance=shop)
        if form.is_valid():
            n = form.save()
            n.status='NotPublished'
            n.save()
            return HttpResponseRedirect(self.request.path_info)

class DeleteShop(View):
    def post(self, request, *args, **kwargs):
        shop = get_object_or_404(Store, owner=request.user,deleted=False)
        shop.deleted=True
        shop.save()
        return redirect(reverse('dashboard'))


class CreateProduct(View):
   
    template_name = 'form/createproduct.html'

    def get(self, request, *args, **kwargs):
        form = ProductCreateForm()
        try:
            shop = get_object_or_404(Store,owner__id = request.user.id,deleted = False)
        except:
            shop = 0
        allow = 1
        if shop and shop.status=="Published":
            allow = 0
        return render(request, self.template_name , {'form': form,'allow':allow,'shop':shop})

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(request.POST, request.FILES)
        shop = Store.objects.filter(owner__id = request.user.id,deleted = False)[0]
        if form.is_valid():
            n = form.save(commit=False)
            n.shop=shop
            n.save()
            return HttpResponseRedirect(self.request.path_info)

class OrderDetail(View):
   
    template_name = 'order-detail.html'

    def get(self, request, *args, **kwargs):
        order = Cart.objects.get(id=self.kwargs['id'])
        cartitems = CartItem.objects.filter(cart=order)

        return render(request, self.template_name , {'cartitems': cartitems})

    def post(self, request, *args, **kwargs):
        shop = Store.objects.get(owner=request.user,deleted=False)
        form = ShopCreateForm(request.POST,instance=shop)
        if form.is_valid():
            n = form.save()
            n.status='NotPublished'
            n.save()
            return HttpResponseRedirect(self.request.path_info)

class Orderlist(View):

    template_name = 'order-list.html'

    def get(self, request, *args, **kwargs):
        orders = Cart.objects.filter(is_paid=True).order_by('-created_at')

        return render(request, self.template_name , {'orders': orders})

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('change'):
            query = self.request.POST.get('change')
            order = Cart.objects.get(id=query)
            if order.accepted == True:
                order.accepted = False
            else:
                order.accepted = True
            order.save()
        
        if self.request.POST.get('from-date') and self.request.POST.get('until-date'):
            print(self.request.POST.get('from-date'))
            frome=self.request.POST.get('from-date')
            until=self.request.POST.get('until-date')
            orders=Cart.objects.filter(created_at__range=[frome, until]).order_by('-created_at')
            return render(request, self.template_name , {'orders': orders})
        
        if self.request.POST.get('accepted'):
            status=self.request.POST.get('accepted')
            orders=Cart.objects.filter(accepted=status).order_by('-created_at')
            filterby='status'
            return render(request, self.template_name , {'orders': orders})


        return HttpResponseRedirect(self.request.path_info)


class myRegister(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm(None or request.POST)
        return render(request, 'form/register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(None or request.POST)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                CustomUser.objects.create_user(
                    form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
                return redirect(reverse('login'))


def login_user(request):
    form = Signin()
    if request.method == "POST":
        form = Signin(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.user_type == "Seller":
                print("logged in")
                login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(request.GET.get('next'))
                return redirect(reverse('dashboard'))

    return render(request, 'form/login.html', {'form': form})