from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
from newsletter_plus.settings import PATH_PROJECT


class Portal(models.Model):
    name = models.CharField(max_length=250, unique=True)
    url = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='')
    image_path = models.CharField(max_length=250)
    likes = models.IntegerField()
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    url = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    news = models.ManyToManyField(News)

    def __str__(self):
        return self.user.username