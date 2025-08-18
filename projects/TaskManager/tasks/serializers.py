from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from tasks.models import Task, User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_staff', 'is_active')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner'] 

    
        
        
class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title', 'description', 'due_date', 'status', 'priority', 'assignee'
        )
        
    def validate_due_date(self, value):
    # Ensure input is timezone-aware
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())
        
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate(self, attrs):
        owner = attrs.get('owner')
        assignee = attrs.get('assignee')

        if owner and assignee and owner == assignee:
            raise serializers.ValidationError("Owner and assignee cannot be the same.")
        return attrs


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'status'
        ]
        
class UpdateAssigneeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'