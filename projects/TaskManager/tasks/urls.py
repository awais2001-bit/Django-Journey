from django.urls import path
from tasks import views

urlpatterns = [
    path('createtask/', views.CreateTask.as_view(), name='create_task'),
    path('mytasks/', views.ViewTask.as_view(), name='update_task'),
    path('updatetask/<int:task_id>/', views.UserUpdateTask.as_view(), name='update_task'),
    path('deletetask/', views.DeleteTask.as_view(), name='delete_task'),
    path('', views.home, name='home'),
    ]
