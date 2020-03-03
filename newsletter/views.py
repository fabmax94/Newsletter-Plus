from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime

from .models import News, Bookmark
from .serializers import NewsSerializer
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


class LastNewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer

    def get_queryset(self):
        portal = self.request.query_params.get('portal')

        return News.objects.filter(portal=portal).order_by('-date')[:10]


class BookmarkUpdateView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request):
        post_data = request.data
        news_id = post_data.get("news_id", None)
        if not News.objects.filter(id=int(news_id)).exists():
            return HttpResponseNotFound()

        news = News.objects.get(id=int(news_id))
        bookmark = None
        if Bookmark.objects.filter(user=request.user).exists():
            bookmark = Bookmark.objects.get(user=request.user)
        else:
            bookmark = Bookmark.objects.create(
                user=request.user
            )

        if bookmark.news.filter(id=news.id).exists():
            bookmark.news.remove(news)
        else:
            bookmark.news.add(news)
        bookmark.save()
        return HttpResponse()


class NewsSaveView(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            if News.objects.filter(title=data['title']).exists():
                return JsonResponse({"message": "already exist"})
            News.objects.create(title=data["title"], content=data["content"], description=data["description"],
                                author=data['author'], date=datetime.now(), likes=0,
                                image_path=data["image"], portal=data['portal'])
            return JsonResponse({"message": "Success"})
        except Exception as exc:
            print(str(exc))
            return JsonResponse({"message": str(exc)})


class BookmarkView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        if Bookmark.objects.filter(user=self.request.user).exists():
            return Bookmark.objects.get(user=self.request.user).news.all()

        return []


class NewsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self, request, pk):
        user = self.request.user
        id_data = int(pk)
        if Bookmark.objects.filter(user=user).exists():
            bookmark = Bookmark.objects.get(user=user)
            is_bookmark = any(
                [news.id == id_data for news in bookmark.news.all()])
        else:
            is_bookmark = False

        queryset = News.objects.all()
        news = get_object_or_404(queryset, pk=pk)
        result = dict(NewsSerializer(news).data)
        result.update({"is_bookmark": is_bookmark})
        return JsonResponse(result)
