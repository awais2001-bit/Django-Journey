from rest_framework import serializers
from .models import User, Organizer, Event, TicketType, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password', 'is_organizer', 'is_participant']
        
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        is_organizer = data.get('is_organizer', False)
        is_participant = data.get('is_participant', True)
        if is_organizer and is_participant:
            raise serializers.ValidationError("User can only be either organizer or participant.")
        if not is_organizer and not is_participant:
            raise serializers.ValidationError("User must be either organizer or participant.")
        return data
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_organizer=validated_data.get('is_organizer', False),
            is_participant=validated_data.get('is_participant', True)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    

