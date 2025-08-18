from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.s

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

class Post(models.Model):
    
    title = models.CharField(max_length=250)
    content = models.TextField(related_name='content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    
class Comment(models.Model):
   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Like(models.Model):
  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['post', 'user'], name='unique_post_like')]
    
class Tag(models.Model):
    
    name = models.CharField(max_length=50, unique=True)