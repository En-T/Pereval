from email.mime import image
from django.db import models
from Pereval.settings import MEDIA_URL

class User(models.Model):
    name = models.CharField(max_length = 64)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 20)


class Coords(models.Model):
    latitude = models.FloatField()
    longtude = models.FloatField()
    height = models.IntegerField()


class Images(models.Model):
    data = models.ImageField(upload_to='uploads')
    date = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 64)


class Pereval(models.Model):

    new = 'n'
    pending = 'p'
    accepted = 'a'
    rejected= 'r'
    
    STATUS = [
        (new, 'Новый'),
        (pending, 'В ожидании'),
        (accepted, 'Принято'),
        (rejected, 'Отклонено')
    ]
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete = models.CASCADE)
    beauty_title = models.CharField(max_length = 64)
    title = models.CharField(max_length = 64)
    other_titles = models.CharField(max_length = 64)
    status = models.CharField(max_length = 1, choices = STATUS, default = new)
    connect = models.TextField()
    add_date = models.DateTimeField(auto_now_add = True)
    l_winter = models.CharField(max_length = 10)
    l_summer = models.CharField(max_length = 10)
    l_autumn = models.CharField(max_length = 10)
    l_spring = models.CharField(max_length = 10)
    images = models.ManyToManyField(Images, through = 'Pereval_Images')
    

class Pereval_Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete = models.CASCADE)
    images = models.ForeignKey(Images, on_delete = models.CASCADE)