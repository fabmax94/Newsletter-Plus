from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from newsletter import views
from newsletter_plus.views import RegistrationAPI, LoginAPI, UserAPI

router = routers.DefaultRouter()
router.register(r'portal', views.PortalView, 'portal_list')
router.register(r'news', views.NewsView, 'news_get')
router.register(r'bookmark', views.BookmarkView, 'bookmark_get')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("auth/register", RegistrationAPI.as_view()),
    path("auth/login", LoginAPI.as_view()),
    path("auth/user", UserAPI.as_view())
]
