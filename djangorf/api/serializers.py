from decimal import Decimal
from rest_framework import serializers
from .models import Product,Order, OrderItem


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
    