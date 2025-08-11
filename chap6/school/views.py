from django.shortcuts import render
from school.models import Student, Teacher
from django.db.models import Q
from django.views import View
from django.views.generic.list import ListView
# Create your views here.

def home(req):
    return render(req, 'school/home.html')

class HomeView(View):
    def get(self, req):
        return render(req, 'school/home.html')

def student_data(req):
    all_data = Student.objects.all()
    #all_data = Student.objects.filter(marks=1015)
    #all_data = Student.objects.exclude(marks=1015)
    #all_data = Student.objects.latest('passdate') # latest pass date will be returned
    #all_data.exists() # returns True if any record exists
    #all_data = Student.objects.order_by('marks') # or '-marks' for descending order [0:5] top five will be shown
    return render(req, 'school/student_data.html', {'students': all_data})


#generic based ListView is used when you want to show a list of objects in a template, the generic view reduces code and improves reusability
class StudentListView(ListView):
    model = Student
    #template_name = 'school/student_list.html'  # specify the template to be used
    def get_queryset(self):
        return Student.objects.filter(marks=1015)

def student_data_field_lookup(req):
    all_data = Student.objects.filter(name__exact='Hamza') # exact match and also u can use iexact if you dont want case sensitive
    #all_data = Student.objects.filter(name__contains='a') # this will show the data which contains 'a' in name
    #all_data = Student.objects.filter(id_in=[1, 2, 3]) # this will show the data which has id in the list
    #all_data = Student.objects.filter(marks_gt=1000) # this will show the data which has marks greater than 1000
    #all_data = Student.objects.filter(name__startswith='a') # this will show the data which has name starting with 'a'
    #all_data = Student.objects.filter(pass_data__range='') #for date
    
    return render(req, 'school/student_data.html', {'students': all_data})

    #all_data = Student.objects.filter(Q(name__exact='Hamza') | Q(marks__gt=1000)) # this will show the data which has name exact 'Hamza' or marks greater than 1000