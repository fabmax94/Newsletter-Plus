from django.contrib import admin

from newsletter.models import News, Bookmark
admin.site.register(News)
admin.site.register(Bookmark)
