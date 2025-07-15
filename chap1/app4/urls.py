from django.urls import path

from app4.views import template_language,template_language_index

urlpatterns = [
    path('template/', template_language_index, name='template_language_index'),
    path('temp_lang/', template_language, name='template_language'),
]