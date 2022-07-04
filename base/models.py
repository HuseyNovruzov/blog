import math
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    classname = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self,email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        username = username
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user 

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    user_avatar = models.ImageField(default='avatar.jpg')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Articles(models.Model):

    host = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(null=True, upload_to='article_images')
    short_description = models.CharField(max_length=250,null=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


    def shortdescription(self):
        
        return self.description[:150].replace('  ', ' ')

class Messages(MPTTModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['-updated', '-created']
    
    def __str__(self):
        return self.body[:50]

    
   


    