from django.urls import path
from school.views import home,student_data

urlpatterns = [
    path('', home, name='home'),
    path('student_data/', student_data, name='student_data'),
]
