from django.shortcuts import render
from student.models import Profile,User
from student.forms import Registrations
from django.http import HttpResponseRedirect
from django.urls import reverse  # <-- better than hardcoding URLs

# Create your views here.
def all_data(req):
    query_set = Profile.objects.all() #query set contains all the data from the Profile model
    return render(req, 'student/all.html',{'students': query_set})

def single_data(req):
    single_detail = Profile.objects.get(pk=1) #get the first record from the Profile model
    #donot use such parameter in get which can give multiple records like name, city etc etc
    return render(req, 'student/single.html', {'single_stu': single_detail})

def registration_form(req):
    if req.method == 'POST':
        form = Registrations(req.POST)
        if form.is_valid():
            print(form.cleaned_data) # Print the cleaned data to the console
            user = User(first_name = form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            user.save()
            #user.delete() to delete data
            
            return HttpResponseRedirect(reverse('success'))  # Redirect to success page after form submission
    else:
        form = Registrations()  # Create an instance of the Registrations form
    #form = Registrations(field_order=['first_name', 'last_name', 'email'])  # Specify the order of fields if needed    
    return render(req, 'student/registration.html', {'form': form})
 
def reg_suceess(req):
    return render(req, 'student/success.html')  # Render a success page after form submission