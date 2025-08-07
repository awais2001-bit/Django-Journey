from django import forms
from teacher.models import Profile


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_name', 'email', 'password']  
        
        
class TeacherRegistration(StudentRegistration): # Inherits from StudentRegistration
    class  Meta(StudentRegistration.Meta):
        fields = ['teacher_name', 'email', 'password']
