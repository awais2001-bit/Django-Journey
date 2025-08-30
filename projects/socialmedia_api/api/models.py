from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    following = models.ForeignKey(User,on_delete=models.CASCADE,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = models.UniqueConstraint(fields=['follower','following'],name='follower-following')
        
        
class Post(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'Public' , 'public',
        PRIVATE = 'Private', 'private'
    author = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    text = models.TextField()
    visibility = models.CharField(choices=Visibility.choices, default=Visibility.PUBLIC)
    like_count = models.PositiveIntegerField()
    comment_count = models.PositiveIntegerField()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Notification(models.Model):
    
    class Verb(models.TextChoices):
        FOLLOWED = 'Followed',
        LIKED = "Liked",
        COMMENTED = 'Commented'
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    verb = models.CharField(choices=Verb.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    