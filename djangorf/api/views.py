from django.shortcuts import get_object_or_404, render
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)