from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from selenium import webdriver

# Create your models here.
from newsletter_plus.settings import PATH_PROJECT


class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='')
    image_path = models.CharField(max_length=250)
    likes = models.IntegerField()

    def __str__(self):
        return self.title
