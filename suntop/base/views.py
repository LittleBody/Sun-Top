from django.http  import HttpResponse
from django.shortcuts import render_to_response


def hello(req):
    template_name='base.html' 
    return render_to_response(template_name,{'hello':'hello'})
