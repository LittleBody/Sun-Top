from django.http  import HttpResponse

#First Start HelloWorld
def hello(req):
    return HttpResponse("Python First." )
	
