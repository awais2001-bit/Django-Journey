from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=True)
    

class Organizer(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    venue_city = models.CharField(max_length=100, db_index=True)
    start_at = models.DateTimeField(db_index=True)
    end_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class TicketType(models.Model):
    class Type(models.TextChoices):
        GENERAL = 'GENERAL', 'General'
        VIP = 'VIP', 'VIP'
        
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types',db_index=True)
    name = models.CharField(max_length=50, choices=Type.choices, default=Type.GENERAL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        CANCELLED = 'CANCELLED', 'Cancelled'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'ticket_type'], name='unique_order_ticket')
        ]
    
    

    