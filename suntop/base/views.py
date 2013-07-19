from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render_to_response


class HelloView(View):
    def get(self,request):
        return render_to_response('base.html',{'hello':'HelloWorld'})
helloView = HelloView.as_view()


