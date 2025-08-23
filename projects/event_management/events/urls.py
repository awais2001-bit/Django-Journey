from django.urls import path
from events import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events',views.EventViewSet,basename='events')
urlpatterns = router.urls

