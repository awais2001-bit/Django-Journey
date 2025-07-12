from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def func(response):
    return HttpResponse("Hello World")

def home(response):
    return HttpResponse("This is the home page")