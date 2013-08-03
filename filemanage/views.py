#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, RequestContext, render
from filemanage.models import File
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
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

def index(request):
    if request.method == "POST" :
        ff = FileForm(request.POST, request.FILES)
        if ff.is_valid():
            fileobj = ff.cleaned_data['filename']
            filename = fileobj.name
            newname = get_hash_key(filename)
	    if File.objects.filter(newname=newname):
		newname = get_hash_key(newname)
            size = fileobj.size
            type = os.path.splitext(filename)[1]
	    userid = request.POST.get('userid')
	    if userid != "None":
		user = User.objects.get(id=userid)
	    else:
		try:
		    user = User.objects.get(username="anonymous")
		except User.DoesNotExist:
		    user = User.objects.create(username="anonymous", email="anonymous@suntop.com", password="anonymous")
	    data = File.objects.create(filename=request.FILES['filename'], newname=newname, size=size, type=type, user=user)

            #缩小图片并保存
	    pro_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]) 
	    abs_filepath = os.path.join(pro_dir, "static", data.filename.name)
	    abs_filepath_resize = os.path.join(pro_dir, "static/img_resize/", '/'.join(data.filename.name.split('/')[1:]))
	    abs_dir_resize = os.path.dirname(abs_filepath_resize)
	    if not os.path.exists(abs_dir_resize):
	        os.makedirs(abs_dir_resize)
	    with Image(filename=abs_filepath) as img:
                with img.clone() as i:
                    i.resize(int(150),int(150))
                    i.save(filename=abs_filepath_resize.format())

            return render_to_response('upload.html', {'newname':newname}, context_instance=RequestContext(request))
        else:
            return HttpResponse("ERROR ENTER")
    else:
        ff = FileForm()
    return render_to_response('index.html', {'ff':ff}, context_instance=RequestContext(request))

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
    filename_resize = filename.replace('img', 'img_resize')
    pic_path = os.path.join('/static', filename)
    pic_resize_path = os.path.join('/static', filename_resize)
    return render_to_response('pic_view.html', {'pic_path':pic_path, 'pic_resize_path':pic_resize_path}, context_instance=RequestContext(request))

@login_required(login_url='/account/login/')
def my_share(request):
    user = request.user
    file_dict = {}
    files = File.objects.filter(user=user)
    for file in files:
        filename = file.filename.name
        file_dict[file.newname] = filename.replace('img','img_resize')
    return render_to_response('my_share.html', {'file_dict':file_dict}, context_instance=RequestContext(request))

def all_share(request):
    file_dict={}
    files = File.objects.all()
    for file in files:
	filename = file.filename.name
	file_dict[file.newname] = filename.replace('img', 'img_resize')
    return render_to_response('my_share.html', {'file_dict':file_dict}, context_instance=RequestContext(request))
