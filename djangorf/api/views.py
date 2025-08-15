from django.shortcuts import get_object_or_404, render
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
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
class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)