from decimal import Decimal
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from uuslug import slugify
from django.db.models import F, Sum



# Create your models here.

USER_TYPE = (('Seller', 'seller'), ('Buyer', 'buyer'))
class CustomUser(AbstractUser):
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE, default='Seller')
    name = models.CharField(max_length=55,blank=True,default="-")
class Store(models.Model):
    STATUS=(
        ("Published","Pub"),
        ("NotPublished","NotPub")
    )
    status = models.CharField(
        max_length = 20,
        choices = STATUS,
        default = 'NotPublished'
        )
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=55)
    owner = models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=False)
    image = models.ImageField(default=0)
    type = models.ForeignKey('StoreCategory',on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=55)
    owner = models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=False)
    image = models.ImageField(blank=True)


    def __str__(self):
        return self.name



class Product(models.Model):
    shop = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    image = models.ImageField(blank=True)
    caption = models.TextField(blank=True)
    category = models.ManyToManyField('Category',related_name='product',blank=True)
    tag = models.ManyToManyField('Tag',blank=True,related_name='product')
    cost = models.IntegerField(blank=True)
    available_count= models.IntegerField(blank=True)
    availablity=models.BooleanField(default=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False,unique=True,blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.name = slugify(self.name, self)
        if self.available_count==0:
            self.availablity=False
        else:
            self.availablity=True
        super(Product, self).save(*args, **kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=55)
    content = models.TextField()
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE,related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self',blank=True,null=True,default=None,related_name='nested_category',on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False,unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Tag(models.Model):
    title = models.CharField(max_length=255)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'id': self.pk})
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,related_name='cart')
    is_paid = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def get_absolute_url(self):
        return reverse('orderdetail', kwargs={'id': self.pk})
    
    def __str__(self):
        return self.user.username

    @property
    def total_price(self):
        return self.cartitem.aggregate(
            total_price=Sum(F('quantity') * F('product__cost'))
        )['total_price'] or Decimal('0')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.quantity==0:
            self.delete()
            return 0
        super(CartItem, self).save(*args, **kwargs)

class StoreCategory(models.Model):
    name = models.CharField(max_length=35)


    def __str__(self):
        return self.name
