from rest_framework import serializers
from .models import User, Post, Comment, Like, Tag


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'content', 'created_at']
        extra_kwargs = {
            'author': {'write_only': True}  # This field is read-only and will not be included in the input data
        }


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_name = serializers.ReadOnlyField(source='author.username') #need to show a specific attribute from the related model
    tags = serializers.StringRelatedField(many=True, read_only=True)    #Is the __str__ representation of the related model exactly what I want to show
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_name', 'created_at', 'updated_at', 'comments', 'tags']
        extra_kwargs = {
            'author': {'write_only': True}
        }
        
        
class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    def get_post_count(self, obj):
        return obj.posts.count() # Use the related_name 'posts' from the Post model
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio','post_count']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        