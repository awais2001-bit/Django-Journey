from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['job','applicant'],name='job-applicant')]
        
    