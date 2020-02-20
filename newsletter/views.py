from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime

from .models import News, Bookmark
from .serializers import NewsSerializer
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required


class LastNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    def get_queryset(self):
        portal = self.request.query_params.get('portal')

        return News.objects.filter(portal=portal).order_by('-date')[:10]



class BookmarkSaveView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request): # Here is the new update comes <<<<
        post_data = request.data
        news_id = post_data.get("news_id", None)
        if not News.objects.filter(id=int(news_id)).exists():
            return HttpResponseNotFound()
        
        news = News.objects.get(id=news_id)
        bookmark = None
        if Bookmark.objects.filter(user=request.user).exists():
            bookmark = Bookmark.objects.get(user=request.user)
        else:
            bookmark = Bookmark.objects.create(
                user=request.user
            )
        
        bookmark.news.add(news)
        bookmark.save()
        return HttpResponse()

class BookmarkView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def get_queryset(self):
        if Bookmark.objects.filter(user=self.request.user).exists():
            return Bookmark.objects.get(user=self.request.user).news.all()
        
        return []
    

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
                                image_path=data["image"], portal=data['portal'])
        
        return JsonResponse({"message": "Success"})
    except Exception as exc:
        print(str(exc))
        return JsonResponse({"message": str(exc)})