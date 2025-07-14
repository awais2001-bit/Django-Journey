from django.shortcuts import render

# Create your views here.

def learn_template(request):
    #return render(req, template_name , context={}, content_type=MIME_TYPE, status=None, using=None)
    return render(request, 'app3/index.html')
