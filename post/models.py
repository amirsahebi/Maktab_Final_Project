from django.db import models
from django.urls import reverse
from uuslug import slugify
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=55)
    image = models.ImageField()
    caption = models.TextField()
    category = models.ManyToManyField('Category',related_name='post')
    tag = models.ManyToManyField('Tag',blank=True,related_name='post')
    owner = models.ForeignKey(User,null=False, on_delete=models.CASCADE,verbose_name='post owner')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False,unique=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.name = slugify(self.name, self)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=55)
    content = models.TextField()
    post = models.ForeignKey(Post,default=None,on_delete=models.CASCADE,related_name='comment')
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


    