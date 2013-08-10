#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, render
from filemanage.models import File
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from wand.image import Image
from wand.display import display
import os, hashlib, string, json

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

def get_newname(filename):
    newname = get_hash_key(filename)
    if File.objects.filter(newname=newname):
        while True:
            newname = get_hash_key(newname)
            if not File.objects.filter(newname=newname):
                break
    return newname

def handle_pic(data):
    pro_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
    file_name = data.filename.name
    abs_filepath = os.path.join(pro_dir, "static", file_name)
    abs_filepath_resize = os.path.join(pro_dir, "static/img_resize/", '/'.join(data.filename.name.split('/')[1:]))
    abs_dir_resize = os.path.dirname(abs_filepath_resize)
    if not os.path.exists(abs_dir_resize):
        os.makedirs(abs_dir_resize)
    with Image(filename=abs_filepath) as img:
        with img.clone() as i:
            i.resize(int(150),int(150))
            i.save(filename=abs_filepath_resize.format())

def index(request):
    if request.method == "POST" :
        ff = FileForm(request.POST, request.FILES)
        if ff.is_valid():
            fileobj = ff.cleaned_data['filename']
            filename = fileobj.name
            newname = get_newname(filename)
            size = fileobj.size
            type = os.path.splitext(filename)[1]
            userid = request.POST.get('userid')
            if userid != "None":
                user = User.objects.get(id=userid)
            else:
                user = User.objects.get_or_create(username="anonymous", email="anonymous@suntop.com", password="anonymous")[0]
            data = File.objects.create(filename=request.FILES['filename'], newname=newname, size=size, type=type, date=timezone.now(), user=user)
            handle_pic(data)
            return render(request, 'upload.html', {'newname':newname})
        else:
            return redirect("/")
    else:
        ff = FileForm()
    return render(request, 'index.html', {'ff':ff})

def delete(request):
    user = request.user
    if request.method == "POST" :
        newname = request.POST.get('newname')
        p = File.objects.get(newname = newname)
        if p.user == user:
            p.delete()
            return redirect("/")
        else:
            return HttpResponse("权限不够!")
    else:
        return redirect("/")

def pic_view(request, newname):
    file = File()
    fileobj = file.getfile_by_newname(newname)
    filename = fileobj.name
    filename_resize = filename.replace('img', 'img_resize')
    pic_path = os.path.join('/static', filename)
    pic_resize_path = os.path.join('/static', filename_resize)
    return render(request, 'pic_view.html', {'pic_path':pic_path, 'pic_resize_path':pic_resize_path})

@login_required(login_url='/account/login/')
def my_share(request):
    user = request.user
    file_dict = {}
    file = File()
    files = file.getfile_by_user(user)
    for file in files:
        filename = file.filename.name
        file_dict[file] = filename.replace('img','img_resize')
    return render(request, 'my_share.html', {'file_dict':file_dict})

def all_share(request):
    file_dict={}
    file = File()
    files = file.getfile_all()
    for file in files:
        filename = file.filename.name
        file_dict[file] = filename.replace('img', 'img_resize')
    return render(request, 'my_share.html', {'file_dict':file_dict})
