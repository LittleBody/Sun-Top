from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, RequestContext, render
from filemanage.models import File
from django import forms
import os, hashlib, string

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['filename']

def get_md5(s):
    s = s.encode('utf8') if isinstance(s, unicode) else s
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def get_hash_key(path):
    code_map = string.ascii_lowercase + string.digits + string.ascii_uppercase
    hkeys = ""
    hex = get_md5(path)
    for i in xrange(0, 8):
        n = int(hex[i*4:(i+1)*4], 16)
        x = 0x0000003D & n
        hkeys += code_map[x]
    return hkeys

def index(request):
    if request.method == "POST" :
        ff = FileForm(request.POST, request.FILES)
        if ff.is_valid():
            fileobj = ff.cleaned_data['filename']
            filename = fileobj.name
            newname = get_hash_key(filename)
            size = fileobj.size
            type = os.path.splitext(filename)[1]
            data = File(filename=request.FILES['filename'], newname=newname, size=size, type=type)
            data.save()
            return render_to_response('upload.html', {'newname':newname})
        else:
            return HttpResponse("ERROR ENTER")
    else:
        ff = FileForm()
    return render_to_response('index.html', {'ff':ff})

def delete(request):
    if request.method == "POST" :
        newname = request.POST.get('newname')
        p = File.objects.get(newname = newname)
        p.delete()
        return redirect("/")
    else:
        return redirect("/")

def pic_view(request, pic_id):
    fileobj = File.objects.get(newname = pic_id).filename
    filename = fileobj.name
    pic_path = os.path.join('/static', filename)
    return render_to_response('pic_view.html', {'pic_path':pic_path})
