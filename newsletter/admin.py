from django.contrib import admin

from newsletter.models import News, Bookmark, Portal

admin.site.register(News)
admin.site.register(Bookmark)
admin.site.register(Portal)
