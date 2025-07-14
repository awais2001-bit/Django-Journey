from django.urls import path

from app4.views import dynamic_view

urlpatterns = [
    path('template/', dynamic_view, name='dynamic_view'),
]