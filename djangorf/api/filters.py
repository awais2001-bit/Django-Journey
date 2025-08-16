import django_filters 
from api.models import Product,Order
from rest_framework import filters

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {'name':['exact', 'icontains'],  # Allows filtering by exact match or substring match  
                  'price':['exact', 'gte', 'lte'],  # Allows filtering by exact price, greater than or equal to, and less than or equal to
                  'stock':['exact', 'gte', 'lte'],  # Allows filtering by exact stock, greater than or equal to, and less than or equal to}
        }
        
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')  # Allows filtering by a range of creation dates
    class Meta:
        model = Order
        fields = {
            'status': ['iexact','icontains'],  # Allows filtering by exact status
            'created_at': ['exact'],  # Allows filtering by exact date, greater than or equal to, and less than or equal to
        }
        