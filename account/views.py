#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response, redirect, RequestContext, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms

class Userform(forms.ModelForm):
    class Meta:
	model = User
	fields = ('username', 'password', 'email')
	widgets = {
	    'password':forms.PasswordInput
	}

class Loginform(forms.ModelForm):
    class Meta:
	model = User
	fields = ('username', 'password')
	widgets = {
            'password':forms.PasswordInput
        }

def registe(request):
    if request.method == "POST":
        uf = Userform(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            User.objects.create_user(username, email, password)
	    user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
	else:
	    error = "1"
	    return render_to_response('registe.html', {'uf':uf,'error':error})
    else :
	uf = Userform()
	return render_to_response('registe.html', {'uf':uf}, context_instance=RequestContext(request))

def user_login(request):
    if request.method == "POST" :
	username = request.POST.get('username')
	password = request.POST.get('password')
	if username is not None and password is not None:
	    user = authenticate(username=username, password=password)
	    if user is not None:
		login(request, user)
		return HttpResponseRedirect('/')
	    else:
		pass
	else:
	    pass
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
