from rest_framework import serializers
from tasks.models import Task, User, Activity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name','last_name', 'email')
        
class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ('id','title','description','status','priority','owner','assignee','created_at')


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    task = serializers.CharField(source="task.title", read_only=True)
    class Meta:
        model = Activity
        fields = [
            'task', 'user', 'action', 'timestamp'
        ]
