from decimal import Decimal
from rest_framework import serializers
from .models import Product,Order, OrderItem
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
                'id',
                  'name',
                  'description',
                  'price',
                  'stock',
                )
    def validate_price(self,value):
        if value <=0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    #product = ProductSerializer()
    product_name = serializers.CharField(source='product.name', read_only=True) #if you want to get only name of the product
    product_price = serializers.DecimalField(max_digits = 10, decimal_places=2, source='product.price', read_only=True) #if you want to get only price of the product  
    class Meta:
        model = OrderItem
        #fields = ('product', 'quantity')
        fields = ('product_name', 'product_price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    def get_total(self, obj):
        order_items = obj.items.all()
        return sum(item.total_price for item in order_items)
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'items',
            'total',
        )
    


class ProductInfoSerializer(serializers.Serializer): 
    #get all products, count, max price
    #This pattern is perfect when you want to return custom combined data — e.g., model records + calculated statistics — in one API call.
    #serializers.Serializer lets you define exactly what the JSON structure should be.
    #The serializer handles nested serialization for the products list.
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField() 
    
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock',
        )
        def validate_price(self,value):
            if value <=0:
                raise serializers.ValidationError("Price must be greater than zero.")
            return value
    


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')
    items = OrderItemCreateSerializer(many=True)
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance = super().update(instance, validated_data) # Update the order instance with the validated data
        
        
        if items_data is not None:
            # Clear existing items, optional depends on requirements
            instance.items.all().delete()
            # Create new items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        
        #It’s a context manager from django.db.transaction.
        # It tells Django:
        # “Everything inside this block should succeed as a single database transaction.
        # If any part fails (raises an exception), roll back everything.”
        with transaction.atomic(): 
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
            return order
    
    class Meta:
        model = Order
        fields = ('user', 'status', 'items')
        extra_kwargs = {
            'user':{'read_only': True},  # Assuming the user is set from the request context
        }