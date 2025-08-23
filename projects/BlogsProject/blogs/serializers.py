from rest_framework import serializers
from .models import User, Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    author_name = serializers.ReadOnlyField(source='author.username') #need to show a specific attribute from the related model
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_name', 'created_at', 'updated_at', 'comments']
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
        

        
        
