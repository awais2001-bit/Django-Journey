from django.contrib import admin
from student.models import Profile, Result
# Register your models here.

#admin.site.register(Profile)
#@admin.register(Profile)  # Register the Profile model with the admin site

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city',)  # Fields to display in the list view
    
    
admin.site.register(Profile, ProfileAdmin)  # Register the Profile model with the custom admin class


@admin.register(Result)  # Register the Result model with the admin site
class ResultAdmin(admin.ModelAdmin):
    list_display = ('marks', 'subject')