"""
URL configuration for chap1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('myfunc/', views.func, name='func'),
    # path('', views.home, name='Home'),
    # path('hello/', views.hello, {'status':'ok'},name='hello'),
    path('a/', include('app2.urls')),
    path('', include('app3.urls')),
    path('app4/', include('app4.urls')),
]
