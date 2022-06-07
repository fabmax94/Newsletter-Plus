from datetime import datetime

from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from rest_framework import viewsets, permissions

from .models import News, Bookmark, Portal
from .serializers import NewsSerializer, PortalSerializer


class PortalView(viewsets.ModelViewSet):
    serializer_class = PortalSerializer
    queryset = Portal.objects.all()


class BookmarkView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        return JsonResponse({"bookmarks": [NewsSerializer(item).data for item in
                                           Bookmark.objects.get(user=request.user).news.all()]})

    def create(self, request):
        post_data = request.data
        news_id = post_data.get("news_id")
        news = News.objects.filter(id=news_id).last()
        if not news:
            return HttpResponseNotFound()

        bookmark = Bookmark.objects.get_or_create(
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
        news = News.objects.filter(pk=pk).last()
        if not news:
            return HttpResponseNotFound()

        is_bookmark = False

        if user.is_authenticated:
            bookmark = Bookmark.objects.prefetch_related("news").filter(user=user).values("news").last()
            if bookmark:
                is_bookmark = any(
                    [n == news for n in bookmark["news"]])

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
