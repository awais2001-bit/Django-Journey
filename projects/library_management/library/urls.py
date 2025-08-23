from rest_framework.routers import DefaultRouter
from library import views

urlpatterns = [
    
]


router = DefaultRouter()
router.register('books',views.BookViewSet,basename='books')
router.register('borrow-records',views.BorrowViewSet, basename='borrow-records')
urlpatterns += router.urls