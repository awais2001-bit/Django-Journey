from django.contrib import admin
from blogs.models import User, Post, Comment, Like

# Register your models here.

admin.site.register(User)
admin.site.register(Post)