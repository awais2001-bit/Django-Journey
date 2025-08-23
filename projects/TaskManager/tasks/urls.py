from django.urls import path
from tasks import views

urlpatterns = [
    path('createtask/', views.CreateTask.as_view(), name='create_task'),
    path('alltasks/', views.AllTasks.as_view(), name='all_tasks'),
    path('mytasks/', views.UserTask.as_view(), name='update_task'),
    path('updatetask/<int:task_id>/', views.UserUpdateTask.as_view(), name='update_task'),
    path('updateassigneetask/<int:task_id>/', views.AdminUpdateTask.as_view())
    ]
