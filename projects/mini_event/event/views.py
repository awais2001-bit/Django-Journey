from event.models import User, Organizer, Event, TicketType, Order, OrderItem
from event.serializers import UserSerializer,OrganizerSerializer, EventSerializer,TicketTypeSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import viewsets,filters,generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum

# Create your views here.


class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    


class OrganizerViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizerSerializer
    queryset = Organizer.objects.select_related('owner')
    permission_classes = [IsAuthenticated]
    
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
    
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_name='mine', url_path='mine')
    def mine(self, request, pk=None):
        try:
            organizer = Organizer.objects.filter(owner=request.user)
        except Organizer.DoesNotExist:
            raise Response({'message':'You do not have an organizer profile.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganizerSerializer(organizer, many=True)
        return Response(serializer.data)
        
    
    
    
class EventViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'ticket_type':
            return TicketTypeSerializer
        return EventSerializer
    
    queryset = Event.objects.select_related('organizer').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['venue_city']
    ordering_fields = ['start_at', 'end_at']
    
    
    #ticket_types
    @action(detail=True, methods=['get','post'], permission_classes=[IsAuthenticated], url_name='ticket_types', url_path='ticket_types')
    def ticket_type(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound("Event not found.")
        
        if request.method == 'GET':
            ticket_types = TicketType.objects.filter(event=event)
            serializer = TicketTypeSerializer(ticket_types, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TicketTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(event=event)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__ticket_type__event').annotate(
            total_quantity=Sum('items__quantity'),
            total_capacity=Sum('items__ticket_type__capacity'),
            total_items=Count('items')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_name='pay', url_path='pay')
    def pay(self, request, pk=None):
        order = self.get_object()

        if order.user != request.user:
            return Response({'error': 'You can only pay for your own orders.'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != 'PENDING':
            return Response({'error': 'Only pending orders can be paid.'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'PAID'
        order.save(update_fields=['status'])
        return Response({'message': 'Order marked as PAID.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='cancel', url_path='cancel')
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.user != request.user:
            return Response({'error': 'You can only cancel your own orders.'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != 'PENDING':
            return Response({'error': 'Only pending orders can be canceled.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for item in order.items.all():
                item.ticket_type.sold = F('sold') - item.quantity
                item.ticket_type.save(update_fields=['sold'])

            order.status = 'CANCELED'
            order.save(update_fields=['status'])

        return Response({'message': 'Order canceled!.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='mine', url_path='mine')
    def mine(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    