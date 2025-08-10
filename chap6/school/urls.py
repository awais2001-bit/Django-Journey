from django.urls import path
from school.views import home,student_data,student_data_field_lookup

urlpatterns = [
    path('', home, name='home'),
    path('student_data/', student_data, name='student_data'),
    path('student_data_field_lookup/', student_data_field_lookup, name='student_data_field_lookup'),
]
