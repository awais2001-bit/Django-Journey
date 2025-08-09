from django.shortcuts import render
from teacher.forms import StudentRegistration,TeacherRegistration
from django.contrib import messages

# Create your views here.

def student_view_form(req):
    if req.method == 'POST':
        form = StudentRegistration(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Student registered successfully!')
    else:
        form = StudentRegistration()
    
    return render(req, 'teacher/studentreg.html', {'form': form})

def teacher_view_form(req):
    if req.method == 'POST':
        form = TeacherRegistration(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Teacher registered successfully!')
    else:
        form = TeacherRegistration()
    return render(req, 'teacher/teacherreg.html', {'form': form})

def home(req):
    context = {'data': 'Welcome to School Management System'}   
    return render(req, 'teacher/home.html', context)

def profile(req,student_id):
    messages.add_message(req, messages.SUCCESS, 'Profile loaded successfully!')
    messages.add_message(req, messages.INFO, 'This is an info message.')
    messages.success(req, 'This is a success message.')
    messages,set_level(req, messages.DEBUG)
    messages.debug(req, 'This is a debug message.') #debug messages are not shown by default in production, you hqave to set the value first and its level is 10 above 10 you can use by default
    student = {'id':student_id}
    return render(req, 'teacher/profile.html',student)



def set_cookie(req):
    response = render(req,'teacher/setcookie.html')
    response.set_cookie('token', 'y11111')
    return response

def get_cookie(req):
    token = req.COOKIES.get('token', 'No cookie found') # if cookie not found then it will return this value
    response = render(req,'teacher/getcookie.html')
    return response
    
def del_cookie(req):
    response = render(req,'teacher/delcookie.html')
    token = req.COOKIES.delete_cookie('token')  # delete the cookie
    return response

#we use signedcookie to make sure that the cookie is not tampered with, we use parameter salt fo that
#req.COOKIES.get_signed_cookie('token', 'No cookie found', salt='my_salt_value') # if cookie not found then it will return this value


