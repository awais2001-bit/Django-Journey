from http.client import HTTPResponse
from django.shortcuts import render
from tasks.models import Task, User
from rest_framework.response import Response 
from tasks.serializers import UserSerializer, TaskSerializer, CreateTaskSerializer,UpdateTaskSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser,BasePermission
# Create your views here.


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CreateTask(generics.CreateAPIView):
    model = Task
    permission_classes = [IsSuperUser]
    serializer_class = CreateTaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ViewTask(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.all()
        if user.is_superuser:
            return qs 
        return qs.filter(assignee=user)

class UpdateTask(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateTaskSerializer
        return TaskSerializer
    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.all()
        return qs.filter(assignee=user)
     