from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    published_date = models.DateTimeField()
    available = models.BooleanField(default=True)
    
    
class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE,related_name="borrow_records")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    
