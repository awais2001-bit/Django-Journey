from django.shortcuts import render
from student.models import Profile

# Create your views here.
def all_data(req):
    query_set = Profile.objects.all() #query set contains all the data from the Profile model
    return render(req, 'student/all.html',{'students': query_set})

def single_data(req):
    single_detail = Profile.objects.get(pk=1) #get the first record from the Profile model
    #donot use such parameter in get which can give multiple records
    return render(req, 'student/single.html', {'single_stu': single_detail})
