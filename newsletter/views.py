from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import NewsSerializer      # add this
from .models import News                     # add this

class NewsView(viewsets.ModelViewSet):       # add this
  serializer_class = NewsSerializer          # add this
  queryset = News.objects.all()              # add this