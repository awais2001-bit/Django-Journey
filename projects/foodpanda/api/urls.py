from rest_framework.routers import DefaultRouter
from api import views

urlpatterns = [
    
]

router = DefaultRouter()
router.register('user',views.UserView,basename='users')




urlpatterns += router.urls
