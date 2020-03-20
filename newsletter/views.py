from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from datetime import datetime

from .models import News, Bookmark, Portal
from .serializers import NewsSerializer, PortalSerializer
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from itertools import groupby


class PortalView(viewsets.ModelViewSet):
    serializer_class = PortalSerializer
    queryset = Portal.objects.all()


class BookmarkView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        if Bookmark.objects.filter(user=request.user).exists():
            return Bookmark.objects.get(user=request.user).news.all()

        return []

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


class NewsView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny, ]

    serializer_class = NewsSerializer

    def list(self, request):
        portal = request.query_params.get('portal')

        if request.query_params.get('portal'):
            news = News.objects.filter(portal__name=portal)
        else:
            news = News.objects.all()

        result = news.order_by('-date')

        if request.query_params.get('last'):
            result = result[:10]

        return JsonResponse({"news": [NewsSerializer(item).data for item in result]})

    def retrieve(self, request, pk):
        user = self.request.user
        if not News.objects.filter(pk=pk).exists():
            return HttpResponseNotFound()

        is_bookmark = False
        id_data = int(pk)

        if user.is_authenticated:
            if Bookmark.objects.filter(user=user).exists():
                bookmark = Bookmark.objects.get(user=user)
                is_bookmark = any(
                    [news.id == id_data for news in bookmark.news.all()])

        news = News.objects.get(pk=pk)
        result = dict(NewsSerializer(news).data)
        result.update({"is_bookmark": is_bookmark})
        return JsonResponse(result)

    def create(self, request):
        try:
            data = request.data
            if News.objects.filter(title=data['title']).exists():
                return JsonResponse({"message": "already exist"})

            if not Portal.objects.filter(name=data['portal']).exists():
                return JsonResponse({"message": "portal is not exist"})

            portal = Portal.objects.get(name=data['portal'])
            News.objects.create(title=data["title"], content=data["content"], description=data["description"],
                                author=data['author'], date=datetime.now(), likes=0,
                                image_path=data["image"], portal=portal, url=data['url'])
            return JsonResponse({"message": "Success"})
        except Exception as exc:
            print(str(exc))
            return JsonResponse({"message": str(exc)})
