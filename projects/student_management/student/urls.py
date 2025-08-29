from rest_framework.urls import path
from rest_framework.routers import DefaultRouter
from student import views


urlpatterns = [
    
]


router = DefaultRouter()
router.register('student',views.StudentView, basename='student')
router.register('teacher',views.TeacherView, basename='teacher')
router.register('course',views.CourseView, basename='course')
router.register('enrollments',views.EnrollmentView, basename='enrollments')
urlpatterns += router.urls
