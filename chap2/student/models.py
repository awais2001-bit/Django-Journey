from django.db import models

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    comments = models.TextField(blank=True, null=True, default='Nothing')