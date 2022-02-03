from django.db import models

class User(models.Model):
    userid = models.CharField(max_length = 50)
    userpw = models.CharField(max_length = 50)

class subway(models.Model):
    global subway
    subwaynum = models.IntegerField()
    subwaysta = models.CharField(max_length = 50)

class arrival(models.Model):
    station = models.CharField(max_length = 50)
    trainline = models.CharField(max_length = 50)
    arrivetime = models.IntegerField()
    trainnum = models.IntegerField()
    waycode = models.CharField(max_length = 50, default = '')

class destination(models.Model):
    startdet = models.CharField(max_length = 50)
    enddet = models.CharField(max_length = 50)

class naviroot(models.Model):
    startline = models.CharField(max_length = 50)
    startwname = models.CharField(max_length = 50)
    startwcode =  models.IntegerField()
    exchaline = models.CharField(max_length = 50)
    exchawname = models.CharField(max_length = 50)
    exchawcode = models.IntegerField()

class subwayim(models.Model):
    substa = models.CharField(max_length = 50)
    subid = models.IntegerField()

class userstatus(models.Model):
    usersta = models.CharField(max_length = 50)
    usertrain = models.IntegerField()

class ocrimg(models.Model):
    title = models.TextField(blank = True, null=True)
    image = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True)

def __str__(self):
        return self.title