from rest_framework import serializers
from .models import User, Organizer, Event, TicketType, Order, OrderItem


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
        fields = ['name', 'bio', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']
    
    

