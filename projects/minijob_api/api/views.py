from django.shortcuts import render
from api.models import User,Company,Job,JobApplication
from api.serializers import JobSerializer,CompanySerializer,RegisterUserSerializer,JobApplicationSerializer
from rest_framework import viewsets,filters,generics
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.



class UserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    model = User


class CompanyViewSet(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]
    model = Company
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
        
        

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related('company').all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    pagination_class = PageNumberPagination
    pagination_class.max_page_size = 10
    pagination_class.page_query_param = 'pagesize'
    filterset_fields = ['location','company']
    
    
    
    
    def get_serializer_class(self):
        #if self.action == 'retrieve':
            #return JobApplicationSerializer
        return  JobSerializer
    
    def perform_create(self,serializer):
        company = serializer.validated_data['company']
        if company.created_by != self.request.user:
            raise PermissionDenied("You do not own this company.")
        serializer.save()
        
        
    @action(detail=True, methods=['post'])
    def apply(self,request,pk=None):
        job = self.get_object()
        
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response({'detail': 'You have already applied'}, status=400)
        
        
        serializer = JobApplicationSerializer(data={
        'job': job.id,
        'applicant': user.id
    })
        serializer.is_valid(raise_exception=True)
        serializer.save()   
        return Response({'detail': 'Application submitted successfully'}, status=201)

        