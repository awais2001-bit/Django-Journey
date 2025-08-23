from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views

urlpatterns = [
    path('companies/',views.CompanyViewSet.as_view(),name='company'),
    path('register/',views.UserView.as_view(),name='user_registration')
]


router = DefaultRouter()
router.register('jobs',views.JobViewSet,basename='jobs')
urlpatterns += router.urls