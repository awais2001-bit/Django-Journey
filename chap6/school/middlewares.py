def my_middleware(get_response):
    print("Middleware initialized")
    
    def middleware(request):
        print("Before view")
        response = get_response(request)
        print("After view")
        return response
    return middleware

    #after making middleware dont forget to add it in settings.py file

class MyMiddleware1:
    def __init__(self, get_response):
        self.get_response = get_response
        print("MyMiddleware initialized")

    def __call__(self, request):
        print("Before view in MyMiddleware")
        response = self.get_response(request)
        print("After view in MyMiddleware")
        return response
class MyMiddleware2:
    def __init__(self, get_response):
        self.get_response = get_response
        print("MyMiddleware2 initialized")

    def __call__(self, request):
        print("Before view in MyMiddleware2")
        response = self.get_response(request)
        print("After view in MyMiddleware2")
        return response
    
class MyMiddleware3:
    def __init__(self, get_response):
        self.get_response = get_response
        print("MyMiddleware3 initialized")

    #process_view is used to process the request before it reaches the view
    #process_exception is used to handle exceptions raised in the view
    #process_template_response is used to process the response before it is rendered
    
    def __call__(self, request):
        print("Before view in MyMiddleware3")
        response = self.get_response(request)
        print("After view in MyMiddleware3")
        return response