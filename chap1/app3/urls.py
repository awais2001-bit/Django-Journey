from django.urls import path
from app3.views import learn_template

urlpatterns = [
    path('learn/', learn_template, name='learn_template'),
]