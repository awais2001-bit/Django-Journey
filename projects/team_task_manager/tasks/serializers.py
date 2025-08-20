from rest_framework import serializers
from tasks.models import Task, User, Activity,Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name','last_name', 'email')
        
        
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Project
        fields = ('name','owner')
        
        
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username',read_only=True)
    assignee = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )    
    class Meta:
        model = Task
        fields = ('id','title','description','status','priority','assignee','owner','created_at')
        


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    task = serializers.CharField(source="task.title", read_only=True)
    class Meta:
        model = Activity
        fields = [
            'task', 'user', 'action', 'timestamp'
        ]
