from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    filename = models.FileField(upload_to='img/%Y/%m/%d')
    newname = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    type = models.CharField(max_length=5)
    user = models.ForeignKey(User, null=True)
