from django.urls import path

from app4.views import dynamic_view, template_language

urlpatterns = [
    path('template/', dynamic_view, name='dynamic_view'),
    path('temp_lang/', template_language, name='template_language'),
]