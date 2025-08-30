from student.models import User,Student,Teacher,Course,Enrollment
from student.serializers import CourseSerializer,StudentSerializer,EnrollmentSerializer,TeacherSerializer
from rest_framework import viewsets,filters,generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
# Create your views here.



class StudentView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = StudentSerializer
    queryset = Student.objects.all().annotate(total_students=Count('roll_number'))
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 5
    pagination_class.page_query_param = 'pagesize'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['name','roll_number']
    lookup_field = 'roll_number'
    lookup_url_kwarg = 'roll_number'
    
    
    @action(detail=True, methods=['get'], url_path='courses', url_name='student-courses')
    def get_student_courses(self, request, roll_number=None):
        try:
            student = self.get_object()
        except Student.DoesNotExist:
            raise NotFound(f"Student with roll_number '{roll_number}' not found.")
        
        enrollments = Enrollment.objects.filter(student=student)
        courses = [enrollment.course for enrollment in enrollments]
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)
    
class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 5
    pagination_class.page_query_param = 'pagesize'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['subject']
    
    
class CourseView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CourseSerializer
    queryset = Course.objects.select_related('teacher').all()
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 5
    pagination_class.page_query_param = 'pagesize'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['teacher']
    
    
class EnrollmentView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.select_related('student','course').all()
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 5
    pagination_class.page_query_param = 'pagesize'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    