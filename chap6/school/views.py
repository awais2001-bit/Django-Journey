from django.shortcuts import render
from school.models import Student, Teacher

# Create your views here.

def home(req):
    return render(req, 'school/home.html')

def student_data(req):
    #all_data = Student.objects.all()
    #all_data = Student.objects.filter(marks=1015)
    #all_data = Student.objects.exclude(marks=1015)
    all_data = Student.objects.order_by('marks') # or '-marks' for descending order [0:5] top five will be shown
    return render(req, 'school/student_data.html', {'students': all_data})

