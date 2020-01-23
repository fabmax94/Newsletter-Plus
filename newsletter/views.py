from rest_framework import viewsets

from .models import News
from .serializers import NewsSerializer


class LastNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-date')[:10]


class BestNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-likes')[:10]


class NewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer

    def get_queryset(self):
        id_data = self.request.query_params.get('id')

        return News.objects.filter(id=id_data)
