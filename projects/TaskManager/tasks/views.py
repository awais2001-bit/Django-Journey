from django.shortcuts import render
from tasks.models import Task, User
from rest_framework.response import Response 
from tasks.serializers import  TaskSerializer, CreateTaskSerializer,UpdateTaskSerializer,UpdateAssigneeTaskSerializer
from rest_framework import generics,filters,status
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser,BasePermission
from rest_framework.views import APIView
from tasks.filters import CustomFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CreateTask(generics.CreateAPIView):
    model = Task
    permission_classes = [IsAuthenticated,IsSuperUser]
    serializer_class = CreateTaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class AllTasks(generics.ListAPIView):
    model = Task
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomFilter
    search_fields = ['title', 'status', 'description', 'assignee__username']
    ordering_fields = ['due_date', 'priority']
    
    


class UserTask(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomFilter
    search_fields = ['title', 'status', 'description']
    ordering_fields = ['due_date', 'priority']
    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.all()
        if user.is_superuser:
            return qs 
        return qs.filter(assignee=user)


class UserUpdateTask(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateTaskSerializer
        return TaskSerializer
    
    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(assignee=user)
    

class AdminUpdateTask(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    serializer_class = UpdateAssigneeTaskSerializer
    def get_queryset(self):
        return Task.objects.all()
    
    
    
    