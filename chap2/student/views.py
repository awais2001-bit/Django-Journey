from django.shortcuts import render
from student.models import Profile
from student.forms import Registrations

# Create your views here.
def all_data(req):
    query_set = Profile.objects.all() #query set contains all the data from the Profile model
    return render(req, 'student/all.html',{'students': query_set})

def single_data(req):
    single_detail = Profile.objects.get(pk=1) #get the first record from the Profile model
    #donot use such parameter in get which can give multiple records like name, city etc etc
    return render(req, 'student/single.html', {'single_stu': single_detail})

def registration_form(req):
    form = Registrations()  # Create an instance of the Registrations form
    #form = Registrations(field_order=['first_name', 'last_name', 'email'])  # Specify the order of fields if needed    
    return render(req, 'student/registration.html', {'form': form})
 
 
