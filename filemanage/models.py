from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

class File(models.Model):
    filename = models.FileField(upload_to='img/%Y/%m/%d')
    newname = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    type = models.CharField(max_length=5)
    date = models.DateTimeField()
    user = models.ForeignKey(User)

    def getfile_by_newname(self, newname):
        fileobj = File.objects.get(newname = newname).filename
        return fileobj

    def getfile_by_user(self, user):
        userid = user.id
        key = "suntop"+":"+"filemanage"+":"+str(userid)
        files = cache.get(key)
        if files:
            return files
        else:    
            files = File.objects.filter(user=user)
            cache.set(key, files, 30)
            return files

    def getfile_all(self):
        key = "suntop:filemanage:all"
        files = cache.get(key)
        if files:
            return files
        else:
            files = File.objects.all()
            cache.set(key, files, 30)
            return files
