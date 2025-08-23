from django.shortcuts import render,get_object_or_404
from catalog.models import User,Category,Cart,CartItem,Order,OrderItem,Product
from catalog.serializers import ProductListSerializer,ProductDetailSerializer,CartItemSerializer,CartSerializer,AdminProductSerializer,OrderCreationSerializer,OrderItemSerializer,OrderSerializer
from rest_framework import generics,viewsets,filters
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission,AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# Create your views here.

class IsSuperUser(BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_superuser)
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['price']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2 
    pagination_class.page_size_query_param = 'page_size'
    pagination_class.max_page_size = 5
    

    def get_permissions(self):
        """
        - Anyone can view (list/retrieve)
        - Only superuser can create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]
    
    
