from rest_framework import viewsets  

from .models import News  
from .serializers import NewsSerializer  


class LastNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer  
    queryset = News.objects.all().order_by('-date')[:10]


class BestNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-likes')[:10]
