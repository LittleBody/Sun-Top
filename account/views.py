#-*- coding:utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from urlparse import urlparse

class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
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
            return redirect('/')
        else:
            user = "None"
            return render(request, 'registe.html', {'uf':uf,'user':user})
    else :
        uf = Userform()
        return render(request, 'registe.html', {'uf':uf})

def user_login(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                user = "None"
                return render(request, 'login.html', {'user':user})
        else:
            user = "None"
            return render(request, 'login.html', {'user':user})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/account/login/')

