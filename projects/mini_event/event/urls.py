from rest_framework.urls import path
from event import views

urlpatterns = [
    path('register/', views.UserViewSet.as_view(), name='user-create'),
]
