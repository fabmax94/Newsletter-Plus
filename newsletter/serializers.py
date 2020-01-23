from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'date', 'author', 'description', 'image')
