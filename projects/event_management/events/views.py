from django.shortcuts import render
from events.models import EventAttendee,User,Events
from events.serializers import EventSerializer,EventDetailSerializer,EventAttendeeSerializer,UserSerializer
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.select_related('created_by').all()
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 10
    pagination_class.page_size_query_param = 'size'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'location':['exact','icontains']}
    search_fields = ['location']
    ordering_fields = ['start_time','end_time']
    permission_classes = [IsAuthenticated]
    
    
    
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'retreive':
            return EventDetailSerializer
        return EventSerializer
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
        
        
    @action(detail=True, methods=['post'])
    def join(self,request,pk=None):
        event = self.get_object()
        user = request.user
        
        if EventAttendee.objects.filter(event=event, user=user).exists():
            return Response({'detail': 'You have already joined this event.'},
                            status=status.HTTP_400_BAD_REQUEST)
            
        EventAttendee.objects.create(event=event, user=user)
        return Response({'detail': 'Joined the event successfully.'},
                        status=status.HTTP_200_OK)
        
    
    @action(detail=True, methods=['post'])
    def leave(self,request,pk=None):
        event = self.get_object()
        user= request.user
        
        attendee =  EventAttendee.objects.filter(event=event, user=user).first()
        if not attendee:
            return Response({'details:You was never in the event'},status=status.HTTP_400_BAD_REQUEST)
        
        attendee.delete()
        return Response({'details:You left the event'},status=status.HTTP_200_OK)
        