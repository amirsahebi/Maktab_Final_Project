from typing import OrderedDict
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
from .models import Cart, Product, Shop

# Create your views here.
class Dashboard(View):
    model1 = Product
    model2 = Cart
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(shop__owner =request.user)
        return render(request, self.template_name , {'products': products})

    # def post(self, request, *args, **kwargs):
    #     updated_request = request.POST.copy()
    #     updated_request.update(
    #         {'post': self.model.objects.get(slug=self.kwargs['slug'])})
    #     form = CommentModelFormView(updated_request)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Comment successfully saved!')
    #         return HttpResponseRedirect(self.request.path_info)

