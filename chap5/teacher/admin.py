from django.contrib import admin
from teacher.models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher_name', 'student_name', 'email', 'password']