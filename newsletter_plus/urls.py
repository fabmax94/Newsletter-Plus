"""newsletter_plus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from newsletter import views
from django.conf.urls.static import static
from newsletter_plus import settings

router = routers.DefaultRouter()
router.register(r'news/last', views.LastNewsView, 'news_last')
router.register(r'news/best', views.BestNewsView, 'news_best')
router.register(r'news/get', views.NewsView, 'news_get')
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include(router.urls)),
                  path('news/save', views.save_news) # TODO: fazer esse request com rest_framework depois
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
