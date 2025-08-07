from django.urls import path
from student.views import all_data, single_data, registration_form,reg_suceess,model_registration_form

urlpatterns = [
    path('all_data/', all_data, name='all_data'),
    path('single_data/', single_data, name='single_data'),   
    path('registration/', registration_form, name='registration_form'),
    path('success/', reg_suceess, name='success'),
    path('model_registration/', model_registration_form, name='model_registration_form'),
]

