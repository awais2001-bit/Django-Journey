from django.urls import path
from django.views.generic.base import TemplateView
from school.views import home,student_data,student_data_field_lookup,HomeView, StudentListView, StudentCreateView,StudentDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('student_data/', student_data, name='student_data'),
    path('student_data_field_lookup/', student_data_field_lookup, name='student_data_field_lookup'),
    path('home_view/', HomeView.as_view(), name='home_view'),
    path('student_list/', StudentListView.as_view(), name='student_list'),
    path('student_create/', StudentCreateView.as_view(), name='student_create'),
    path('thanks/', TemplateView.as_view(template_name='school/thanks.html'), name='thanks1'),
    path('student_delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
]
