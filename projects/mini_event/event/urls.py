from rest_framework.urls import path
from event import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', views.UserViewSet.as_view(), name='user-create'),
]


router = DefaultRouter()
router.register(r'organizers', views.OrganizerViewSet, basename='organizers')
router.register(r'events', views.EventViewSet, basename='events')
urlpatterns += router.urls