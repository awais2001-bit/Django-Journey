from rest_framework import serializers
from events.models import User,Events,EventAttendee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Events
        fields = ('id', 'title', 'location', 'start_time', 'end_time', 'created_by')
        
    def validate(self, data):
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data
        
        
class EventAttendeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = EventAttendee
        fields = ['username', 'email', 'joined_at']
        

class EventDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    attendees = EventAttendeeSerializer(many=True, source='eventattendee_set', read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'location', 'start_time', 'end_time', 'created_by', 'attendees']
