from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
 
class User(AbstractUser):
    pass


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'pending'
        IN_PROGRESS = 'In_Progress', 'inprogress'
        COMPLETED = 'Completed', 'completed'
        
    class Priority(models.TextChoices):
        LOW = 'Low', 'low'
        MEDIUM = 'Medium', 'medium'
        HIGH = 'High', 'high'
        
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.LOW)
        
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)


#optional    
class Activity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)   # e.g., "created", "assigned", "completed"
    timestamp = models.DateTimeField(auto_now_add=True)

    