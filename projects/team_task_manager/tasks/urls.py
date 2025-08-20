from django.urls import path
from tasks import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('projects/', views.ProjectViewSet.as_view(), name='project-list'),
    path('projects/<int:project_id>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/tasks/', views.ProjectTasksView.as_view(), name='task')
]
