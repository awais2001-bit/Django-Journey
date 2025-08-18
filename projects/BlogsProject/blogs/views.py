from django.shortcuts import render
from blogs.serializers import UserSerializer, PostSerializer, CommentSerializer
from blogs.models import User, Post, Comment
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated,IsAdminUser, AllowAny

# Create your views here.

class CreatePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    model = Post
    #permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        qs = Post.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(author=user)
    
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    model = Post
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    #permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        qs = Post.objects.all()
        return qs.filter(author=user)
    
class CreateCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    model = Comment
    #permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().filter(id=self.kwargs.get('post_id'))
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        return serializer.save(author=self.request.user, post=post)