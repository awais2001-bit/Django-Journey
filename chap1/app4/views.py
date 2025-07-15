from django.shortcuts import render
from datetime import datetime

# Create your views here.


#varibles example

# def dynamic_view(request):
#     #business logic here
#     profile = {'name':'awais'}
#     return render(request, 'app4/index.html', context= profile)



def template_language(request):
    return render(request, 'app4/temp.html', context={
        'name': 'Awais',
        'age': 30,
        'hobbies': ['coding', 'reading', 'gaming'],
        'time': datetime.now(),
        'float_value': 3.14159,
        'nm':False,
    })



