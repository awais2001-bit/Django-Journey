from django.urls import path
from teacher.views import student_view_form,teacher_view_form, home,profile


urlpatterns = [
    path('studentreg/', student_view_form, name='studentreg'),
    path('teacherreg/', teacher_view_form, name='teacherreg'),
    path('', home, name='home'),
    path('profile/<int:student_id>', profile, name='profile'), #dynamic url and int is used for striction of id only
]                                                               #slug will be used for larger string 

