from django.shortcuts import render
from events.models import EventAttendee,User,Events
from events.serializers import EventSerializer,EventDetailSerializer,EventAttendeeSerializer,UserSerializer
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
# Create your views here.


