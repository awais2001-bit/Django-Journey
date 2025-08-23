from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.


class User(AbstractUser):
    pass

class Events(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('Start time must be before end time')
        
class EventAttendee(models.Model):
    event = models.ForeignKey(Events,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['event','user'],name='user-event')]