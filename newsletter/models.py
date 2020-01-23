from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='')
    likes = models.IntegerField()

    def __str__(self):
        return self.title


class Link(models.Model):
    url = models.CharField(max_length=550)
    already_read = models.BooleanField()

    def __str__(self):
        return self.url


@receiver(pre_save, sender=Link)
def my_callback(sender, instance, *args, **kwargs):
    response_text = requests.get(instance.url).content.decode("utf-8")
    content = response_text[response_text.find("<article"):response_text.find("</article>") + 10]
    title = response_text[response_text.find("<h1"):]
    title = title[title.find(">")+1:title.find("</h1>")]
    description = response_text[response_text.find("<h2"):]
    description = description[description.find(">") + 1:description.find("</h2>")]
    News.objects.create(title=title, content=content, description=description, author=User.objects.get(username="fabmax"), date=datetime.now(), likes=0)