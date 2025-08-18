import django_filters
from rest_framework import filters
from tasks.models import Task

class CustomFilter(django_filters.FilterSet):
    class Meta:
        model = Task  # This should be set in the view
        fields = {
            'title': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'priority': ['exact', 'icontains'],
            'due_date': ['exact', 'gte', 'lte'],
            'assignee__username': ['exact', 'icontains'],
        }
    