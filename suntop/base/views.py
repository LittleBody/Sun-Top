# Create your views here.
from django.http  import HttpResponse


def hello(req):
    return HttpResponse("Python First." )
	
