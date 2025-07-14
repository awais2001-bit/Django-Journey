from django.urls import path
from app1.views import func, home

urlpatterns = [
    path('func/', func, name='func'),
    path('home/', home, name='home'),
]