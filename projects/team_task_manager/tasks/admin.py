from django.contrib import admin
from tasks.models import User, Project, Task, Activity

# Register your models here.

@admin.register(User)
class UserAmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):   
    list_display = ('name', 'owner')
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'owner', 'assignee', 'created_at')
    
