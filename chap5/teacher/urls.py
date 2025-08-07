from django.urls import path
from teacher.views import student_view_form,teacher_view_form


urlpatterns = [
    path('studentreg/', student_view_form, name='studentreg'),
    path('teacherreg/', teacher_view_form, name='teacherreg'),
]

