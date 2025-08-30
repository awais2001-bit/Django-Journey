from api.models import User,Restaurant,MenuItem,Order,OrderItem
from api.serializers import UserSerializer,OrderItemSerializer,OrderSerializer,MenuItemSerializer,RestaurantSerializer
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



class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    
    
class RestaurantView(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        query_set = Restaurant.objects.select_related('owner').filter(owner=user)
        return query_set