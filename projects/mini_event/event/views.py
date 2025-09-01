from event.models import User, Organizer, Event, TicketType, Order, OrderItem
from event.serializers import UserSerializer,OrganizerSerializer
from rest_framework import viewsets,filters,generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# Create your views here.


class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    


class OrganizerViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizerSerializer
    queryset = Organizer.objects.select_related('owner')
    permission_classes = [IsAuthenticated]
    
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_name='mine', url_path='mine')
    def mine(self, request, pk=None):
        try:
            organizer = Organizer.objects.filter(owner=request.user)
        except Organizer.DoesNotExist:
            raise NotFound("Organizer not found.")
        
        if organizer.owner != request.user:
            raise PermissionDenied("You do not have permission to access this organizer.")
        
        serializer = self.get_serializer(organizer)
        return Response(serializer.data)
    
    
