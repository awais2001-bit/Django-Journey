from django.shortcuts import get_object_or_404, render
from tasks.serializers import UserSerializer, ProjectSerializer, TaskSerializer, UpdateTaskSerializer, RegisterSerializer
from tasks.models import User, Project, Task, Activity
from rest_framework.decorators import api_view,action
from rest_framework.response import Response 
from django.db.models import Max, Q
from rest_framework import generics,filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser,BasePermission
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# Create your views here.


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class UserSerializer(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    model = User
    permission_classes = [AllowAny]

class ProjectViewSet(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    model = Project
    permission_classes = [IsSuperUser,IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        qs = Project.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(owner=user)
    
    @method_decorator(cache_page(15, key_prefix="projects_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    model = Project
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'
    permission_classes = [IsSuperUser,IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        qs = Project.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(owner=user)
    
class ProjectTasksView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        get_object_or_404(Project, id=project_id)
        queryset = Task.objects.filter(project_id=project_id).select_related('project', 'owner', 'assignee')
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        serializer.save(owner=self.request.user, project=project)
    
    @method_decorator(cache_page(5, key_prefix="tasks_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        

class TaskViewSet(generics.RetrieveUpdateDestroyAPIView):
    model = Task
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs.get('task_id')
        get_object_or_404(Task, id=task_id)
        query_set = Task.objects.filter(Q(id=task_id) & (Q(assignee=user) | Q(owner=user))).select_related('project', 'owner', 'assignee').prefetch_related('activities')
        return query_set
    
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return UpdateTaskSerializer
        return TaskSerializer