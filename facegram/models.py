from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    photo = models.ImageField(upload_to='profile',default='profile/avtar.jpg')
    bio  = models.CharField(max_length=255,blank=True)
    account_type  = models.CharField(max_length=255,default='public')
    following  =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_following')
    follower  =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_follower')

# User.add_to_class('photo', models.ImageField(upload_to='profile',default='profile/avtar.jpg'))
# User.add_to_class('bio', models.CharField(max_length=255,blank=True))
# User.add_to_class('account_type', models.CharField(max_length=255,default='public'))
# User.add_to_class('following',models.ManyToManyField(User,blank=True,related_name='user_following'))
# User.add_to_class('follower',models.ManyToManyField(User,blank=True,related_name='user_follower'))

class Post(models.Model):
    title = models.CharField(max_length=255)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='CASCADE')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,blank=True,related_name='like_posts')
    def __str__(self):
        return self.title

class Photo(models.Model):
    photo = models.ImageField(upload_to='photos')
    post = models.ForeignKey(Post, on_delete='CASCADE',
                             related_name='my_photo')

class Comment(models.Model):
    content =models.CharField(max_length=255)
    actor =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='CASCADE')
    post = models.ForeignKey(Post,on_delete='CASCADE',related_name='my_comments')
    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

class Story(models.Model):
    story = models.ImageField(upload_to='story')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='CASCADE',related_name='my_story')
    postdate = models.DateTimeField(auto_now_add=True)




    




