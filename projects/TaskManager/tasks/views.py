from http.client import HTTPResponse
from django.shortcuts import render
from tasks.models import Task, User
from rest_framework.response import Response 
from tasks.serializers import UserSerializer, TaskSerializer, CreateTaskSerializer,UpdateTaskSerializer
from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser,BasePermission
from rest_framework.views import APIView
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
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DeleteTask(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, *args, **kwargs):
        query_set = Task.objects.filter(status="completed")
        serializer = TaskSerializer(query_set, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        queryset = Task.objects.filter(status="completed")
        count = queryset.count()
        if count == 0:
            return Response({"message": "No completed tasks found."}, status=status.HTTP_404_NOT_FOUND)
        
        queryset.delete()
        return Response({"message": f"{count} completed tasks deleted."}, status=status.HTTP_200_OK)

    