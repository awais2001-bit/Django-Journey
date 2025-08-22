from rest_framework import serializers
from catalog.models import User,Category,Cart,CartItem,Order,OrderItem,Product




class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ('id','name','sku','price','category','inventory_count')
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','description')
        
        
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "price", "description", "category", "inventory_count")
        

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name',read_only=True)
    class Meta:
        model = CartItem
        fields = ('product_id','product_name','quantity','price_at_addition')
        
    def validate_quantity(self,value):
        if value <=0:
            raise serializers.ValidationError('Quantity is zero!!')
        return value
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ('id','owner','items')
        

class OrderCreationSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ('cart_id','shipping_info')
        
    def validate_cart_id(self,value):
        try:
            cart = Cart.objects.get(id=value)
        except cart.DoesNotExist:
            raise serializers.ValidationError('cart does not exist')
        
        if not cart.items.exist():
            raise serializers.ValidationError('Empty Cart')
            


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name','description','price','inventory_count','sku','category')
        
        
    def validate_price(self,value):
        if value <=0:
            raise serializers.ValidationError('Price must be above 0')
        return value
        
    def validate_inventory_count(self,value):
        if value <=0:
            raise serializers.ValidationError('Nothing in inventory!!')
        return value
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    sub_total = serializers.SerializerMethodField()
    
    
    class Meta:
        model = OrderItem
        fields = ("product_name", "unit_price", "quantity", "sub_total")    
        
    def get_subtotal(self,obj):
        return obj.unit_price * obj.quantity
    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ("id", "status", "created_at", "items", "total_amount", "shipping_info")

    def get_total_amount(self, obj):
        return sum(item.unit_price * item.quantity for item in obj.items.all() )