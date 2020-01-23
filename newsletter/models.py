from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
from newsletter_plus.settings import PATH_PROJECT


class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='')
    image_path = models.CharField(max_length=250)
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
    proxies = {'http': 'http://105.112.150.10:8080', 'https': 'http://105.112.150.10:8080'}
    response_text = requests.get(instance.url, proxies=proxies, verify=False).content.decode("utf-8")
    content = response_text[response_text.find("<article"):response_text.find("</article>") + 10]
    title = response_text[response_text.find("<h1"):]
    title = title[title.find(">") + 1:title.find("</h1>")]
    description = response_text[response_text.find("<h2"):]
    description = description[description.find(">") + 1:description.find("</h2>")]
    image = response_text[response_text.find("<figure"):]
    image = image[image.find('<img') + 10:]
    image = image[image.find('<img'):]
    image = image[image.find('src="') + 5:]
    image = image[:image.find('"')]
    News.objects.create(title=title, content=content, description=description,
                        author=User.objects.get(username="fabmax"), date=datetime.now(), likes=0,
                        image_path=image)
