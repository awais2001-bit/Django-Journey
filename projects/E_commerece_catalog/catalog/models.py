from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.core.validators import MinValueValidator
# Create your models here.

class User(AbstractUser):
    pass
    
    
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True,db_index=True)
    description = models.TextField(null=True)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sku = models.CharField(unique=True,db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    

    
class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100,null=True,blank=True)
    
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_addition = models.DecimalField(max_digits=10,decimal_places=2)
    
    
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        CANCELLED = 'cancelled', 'Cancelled'
        FULFILLED = 'fulfilled', 'Fulfilled'
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_info = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    
    @property
    def sub_total(self):
        return Decimal(self.quantity) * Decimal(self.unit_price)
    
    
    
        
    
    
    