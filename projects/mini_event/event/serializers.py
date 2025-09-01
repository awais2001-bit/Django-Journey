from rest_framework import serializers
from .models import User, Organizer, Event, TicketType, Order, OrderItem
from django.db import transaction
from django.db.models import F

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password']
        
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    

class OrganizerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Organizer
        fields = ['id','name', 'bio', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']
    
    


class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    organizer_id = serializers.PrimaryKeyRelatedField(queryset=Organizer.objects.all(), source='organizer', write_only=True)
    class Meta:
        model = Event
        fields = ['id','title', 'description', 'organizer','organizer_id', 'venue_city', 'start_at', 'end_at', 'is_published', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def validate_organizer(self, value):
        request = self.context.get('request')
        if value.owner != request.user:
            raise serializers.ValidationError("You do not own this organizer.")
        return value
    
    def validate(self, attrs):
        if attrs['start_at'] >= attrs['end_at']:
            raise serializers.ValidationError("Event end time must be after start time.")
        return attrs
    
    
class TicketTypeSerializer(serializers.ModelSerializer):
    event = serializers.CharField(source='event.id')
    class Meta:
        model = TicketType
        fields = ['id', 'event', 'name', 'price', 'capacity', 'sold']
        read_only_fields = ['id', 'sold']
        
    def validate_event(self, value):
        request = self.context.get('request')
        if value.organizer.owner != request.user:
            raise serializers.ValidationError("You do not own this event.")
        return value
    
    
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    ticket_type = serializers.CharField(source='tickettype.name')
    class Meta:
        model = OrderItem
        fields = ['id', 'ticket_type', 'quantity']
        read_only_fields = ['id']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        
        
        

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class OrderItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ['ticket_type', 'quantity']
    items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        validated_data.pop('user',None)
        order = Order.objects.create(user=user, status='PENDING', **validated_data)
            
        for item_data in items_data:
                ticket_type = item_data['ticket_type']
                quantity = item_data['quantity']
                ticket_type.sold = F('sold') + quantity
                ticket_type.save(update_fields=['sold'])
                OrderItem.objects.create(order=order, **item_data)
        return order
    class Meta:
            model = Order
            fields = ['id', 'user', 'status', 'items', 'created_at']
            read_only_fields = ['id', 'user', 'status', 'created_at']
    

    