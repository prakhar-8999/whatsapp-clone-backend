# from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class phone_num(models.Model):
    phone = models.CharField(max_length=10)
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images',default="images/default.png")
    nick_name = models.CharField(max_length=20,default="")

class messages(models.Model):
    message=models.TextField()
    sender=models.IntegerField()
    receiver=models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)