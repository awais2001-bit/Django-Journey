from django.urls import path
from student.views import all_data, single_data, registration_form

urlpatterns = [
    path('all_data/', all_data, name='all_data'),
    path('single_data/', single_data, name='single_data'),   
    path('registration/', registration_form, name='registration_form'),
]
