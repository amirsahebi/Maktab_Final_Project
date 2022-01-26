from unicodedata import name
from django.urls import reverse
from datetime import date
from django.http import response
from rest_framework.test import APITestCase
from model_mommy import mommy

from shop.models import Cart, CustomUser, Product, Profile, Store

from django.test import TestCase
from django.conf import settings

from shop.serializers import CartCreateSerializer



class ApiTestCase(APITestCase):

    def setUp(self):
        self.user = mommy.make(CustomUser, user_type="Buyer")
        self.profile = mommy.make(Profile,name="test",owner=self.user)
        self.shop = mommy.make(Store,name="test",owner=self.user)
        self.product = mommy.make(Product,name="test",shop=self.shop,cost=200,available_count=2)
        self.cart = mommy.make(Cart,user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_register(self):
      # right input
        resp = self.client.post(reverse('api-register'),{'username':'testperson','email':'testperson@gmail.com','password':'test1234'})
      # wrong input
        resp2 = self.client.post(reverse('api-register'),{'username':'testperson','email':'testperson@gmail.com','password':'test1'})

        self.assertEqual(resp.status_code,201)
        self.assertEqual(resp2.status_code,400)


    def test_profile(self):
        resp = self.client.get(reverse('profile'))
        resp2 = self.client.post(reverse('profile'),data={
            "name":"test",
            "image": "",
        })
        resp3 = self.client.put(reverse('profile'),data={
            "name":"test2",
            "image": "",
        })


        
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp2.status_code,200)
        self.assertEqual(resp3.status_code,200)


    
    def test_cart(self):
        
        resp = self.client.post(reverse('createcart'),data={
            "product":self.product.pk
        })

        self.assertEqual(resp.status_code,201)

      #test_addtocart

        resp2 = self.client.post(reverse('addtocart'),data={
            "product":self.product.pk
        })

        self.assertEqual(resp2.status_code,201)

      #test_deletecartitem

        resp3 = self.client.post(reverse('deletecartitem'),data={
            "product":self.product.pk
        })
        

        self.assertEqual(resp3.status_code,201)

      #test_paycart

        resp4 = self.client.post(reverse('paycart'),data={})

        self.assertEqual(resp4.status_code,200)

      #test_paidcart

        resp5 = self.client.get(reverse('paidcarts'))

        self.assertEqual(resp5.status_code,200)


    def test_store(self):

      #test_published_store  

        resp = self.client.get(reverse('store'))

        self.assertEqual(resp.status_code,200)

      #test_store_categories

        resp2 = self.client.get(reverse('storecategory'))

        self.assertEqual(resp2.status_code,200)

      #test_store_products

        resp3 = self.client.get(reverse('storeproduct',kwargs={'id': 1}))

        self.assertEqual(resp3.status_code,200)

    def test_sms(self):

        resp = self.client.post(reverse('sendcode'),data={'phone':'09123456789'})

        resp2 = self.client.post(reverse('phone-api-register'),data={'phone':'09123456789','token':resp.data['token']})

        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp2.status_code,201)








