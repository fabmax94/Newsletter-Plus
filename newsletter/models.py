from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title
