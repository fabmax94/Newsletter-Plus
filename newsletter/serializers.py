from rest_framework import serializers
from .models import News, Portal


class NewsSerializer(serializers.ModelSerializer):
    portal_name = serializers.CharField(source='portal.name')
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'date', 'author', 'description', 'image', 'image_path', 'portal_name')


class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portal
        fields = ('id', 'name')