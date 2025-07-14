from django.shortcuts import render

# Create your views here.

def dynamic_view(request):
    #business logic here
    profile = {'name':'awais'}
    return render(request, 'app4/index.html', context= profile)