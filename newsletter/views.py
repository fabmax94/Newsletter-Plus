from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime

from .models import News
from .serializers import NewsSerializer
from django.http import JsonResponse


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


# TODO: mudar para ModelViewSet
@csrf_exempt
def save_news(request):
    try:
        data = request.POST.dict()
        if News.objects.filter(title=data['title']).exists():
            return JsonResponse({"message": "already exist"})    
        News.objects.create(title=data["title"], content=data["content"], description=data["description"],
                                author=data['author'], date=datetime.now(), likes=0,
                                image_path=data["image"])
        
        return JsonResponse({"message": "Success"})
    except Exception as exc:
        print(str(exc))
        return JsonResponse({"message": str(exc)})