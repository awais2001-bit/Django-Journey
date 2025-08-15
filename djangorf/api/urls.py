from django.urls import path
from api import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('product-info/', views.product_info, name='product_info'),
    path('productsview/', views.ProductListApiView.as_view(), name='product_list_api'),
    path('productsview/<int:pk>/', views.ProductDetailApiView.as_view(), name='product_detail_api'),
    path('ordersview/<slug:order_id>/', views.OrderDetailApiView.as_view(), name='order_list_api'),
    path('user-orders/', views.UserOrderListApiView.as_view(), name='user_order_list_api'),
    path('productapiview-info/', views.ProductInfoApiView.as_view(), name='product_api_info'),
]