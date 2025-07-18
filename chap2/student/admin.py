from django.contrib import admin
from student.models import Profile
# Register your models here.

#admin.site.register(Profile)
#@admin.register(Profile)  # Register the Profile model with the admin site
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city', 'comments')  # Fields to display in the list view
    
    
admin.site.register(Profile, ProfileAdmin)  # Register the Profile model with the custom admin class
