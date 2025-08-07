from django.shortcuts import render
from teacher.forms import StudentRegistration,TeacherRegistration

# Create your views here.

def student_view_form(req):
    if req.method == 'POST':
        form = StudentRegistration(req.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentRegistration()
    
    return render(req, 'teacher/studentreg.html', {'form': form})

def teacher_view_form(req):
    if req.method == 'POST':
        form = TeacherRegistration(req.POST)
        if form.is_valid():
            form.save()
    else:
        form = TeacherRegistration()
    return render(req, 'teacher/teacherreg.html', {'form': form})

def home(req):
    context = {'data': 'Welcome to School Management System'}   
    return render(req, 'teacher/home.html', context)

def profile(req,student_id):
    student = {'id':student_id}
    return render(req, 'teacher/profile.html',student)