from django.shortcuts import get_object_or_404
from api.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, CreateProductSerializer
from rest_framework.decorators import api_view,action
from rest_framework.response import Response 
from django.db.models import Max
from rest_framework import generics,filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend,OrderFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

# A decorator from Django REST Framework (from rest_framework.decorators import api_view).
# It turns a normal Django view into a DRF view.
# It also restricts which HTTP methods your view will accept — here only GET.

@api_view(['GET']) 
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) #many means we have more than 1 data in query set
    #return JsonResponse({
        #'data': serializer.data,}
        
    return Response(serializer.data)  # Use Response from rest_framework to return serialized data
    
@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    #A Django shortcut function (from django.shortcuts import get_object_or_404).
    #Tries to fetch an object from the database.
    #If found → returns the object.
    #If not found → automatically raises an HTTP 404 error.
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items__product').all() #prefetch_related is used to optimize database queries by fetching related objects in a single query
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': products.count(),
        'max_price': products.aggregate(max_price = Max('price')) ['max_price']
    })
    
    return Response(serializer.data)






#GENERIC VIEWS





class ProductListApiView(generics.ListAPIView): #ListAPIView Get all objects
    #queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)  #if you want to filter products that are in stock
    serializer_class = ProductSerializer
    
class ProductDetailApiView(generics.RetrieveAPIView): #RetrieveAPIView Get only one object
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Allows us to use the primary key in the URL to retrieve a specific product
    lookup_url_kwarg = 'pk'  # This matches the URL pattern where pk is used as a variable by default it is pk but you can change it also on the basis of what you want to use in urls.py
    
class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()  # Prefetch related to optimize database queries
    serializer_class = OrderSerializer
    
    
class OrderDetailApiView(generics.RetrieveAPIView): 
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'  # Allows us to use the order_id in the URL to retrieve a specific order
    lookup_url_kwarg = 'order_id'  # This matches the URL pattern where order_id is used as a variable
    
    
    
# in this class we are using session based authentication, so we can access the user from request.user and we can see the orders of the user who is logged in
# At that point, there is no self.request — the view hasn’t even been created yet.
# So, you can’t use request-dependent data like self.request.user in queryset.
# In short:
# queryset → Static, evaluated once when the server starts
# get_queryset() → Dynamic, evaluated for each request
# That’s why get_queryset() is the clean, safe, and recommended way for user-specific or parameter-based queries.

class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)
    
    
    
class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': products.count(),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
    
class ProductCreateApiView(generics.CreateAPIView):
    model = Product
    serializer_class = CreateProductSerializer
    
    
class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
            
        return super().get_permissions()
    


class ProductAllView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'  # This matches the URL pattern where pk is used as a variable by default it is pk but you can change it also on the basis of what you want to use in urls.py
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

class ProductFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['name', 'price']  # Allows filtering by name and price in the API, this is used # to filter the products in the API, you can use this in the URL like this: /products/listcreate?name=product_name
    #we can use this filter instead of using get_queryset method, this is used to filter the products in the API,
    #one problem with this is that it is case sensitive
    
    
    #filterset_class = ProductFilter  #we can use the custom filter class defined in api/filters.py, this custom filter also gives us the option to filter by substring too, see the file
    
    

class ProductSearchFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter  # Use the custom filter class defined in api/filters.py
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Enables filtering and searching
    search_fields = ['name', 'description']  # Allows searching by name and description in the API
    
    
class ProductOrderFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter  # Use the custom filter class defined in api/filters.py
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # Enables filtering and searching
    search_fields = ['name', 'description']  # Allows searching by name and description in the API
    ordering_fields = ['price', 'stock']  # Allows ordering by price and stock in the API
    
class ProductCustomFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,InStockFilterBackend]  
    search_fields = ['name', 'description']  
    ordering_fields = ['price', 'stock']  
    
    
class ProductPagePagination(generics.ListAPIView):
    queryset = Product.objects.order_by('pk')  # Order by primary key to ensure consistent pagination
    serializer_class = ProductSerializer
    filterset_class = ProductFilter  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,InStockFilterBackend]  
    search_fields = ['name', 'description']  
    ordering_fields = ['price', 'stock']  
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2  # Set the page size for pagination  
    pagination_class.page_size_query_param = 'page_size'  # Allows clients to set the page size via a query parameter   
    pagination_class.page_size_query_param = 'size' # Allows clients to set the page size via a query parameter
    pagination_class.max_page_size = 10  # Set a maximum page size to prevent abuse  
    
    
class ProductLimitOffsetPagination(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,InStockFilterBackend]  
    search_fields = ['name', 'description']  
    ordering_fields = ['price', 'stock']  
    pagination_class = LimitOffsetPagination
     
    
#viewset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Allow any user to access this viewset, you can change it to IsAuthenticated or IsAdminUser based on your requirements
    
    
class OrderViewFilterSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny] 
    filterset_class = OrderFilter  # Use the custom filter class defined in api/filters.py
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    
    @action(detail=False, methods=['get'], url_path='my-orders')
    def user_orders(self,request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    