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
from newsletter_plus.views import RegistrationAPI, LoginAPI, UserAPI

router = routers.DefaultRouter()
router.register(r'portal', views.PortalListView, 'portal_list')
router.register(r'news', views.NewsListView, 'news_list')
router.register(r'news/get', views.NewsView, 'news_get')
router.register(r'news/save', views.NewsSaveView, 'news_get')
router.register(r'bookmark/get', views.BookmarkView, 'bookmark_get')
router.register(r'bookmark/update',
                views.BookmarkUpdateView, 'bookmark_update')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("auth/register", RegistrationAPI.as_view()),
    path("auth/login", LoginAPI.as_view()),
    path("auth/user", UserAPI.as_view())
]
