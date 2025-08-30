from rest_framework import serializers
from api.models import User,Job,JobApplication,Company


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email')
        


class CompanySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)
    class Meta:
        model = Company
        fields = ('id','name','description','created_by')
    
    
class JobSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
    queryset=Company.objects.all(),
    slug_field='name'  
)

    class Meta:
        model = Job
        fields = ('title','description','company','location','created_at')
        

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('job','applicant','cover_letter','applied_at')
        
        