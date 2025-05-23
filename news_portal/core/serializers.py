from rest_framework import serializers
from .models import Article, Publisher, User

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'bio']

class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        # Only include journalists, assuming role='JOURNALIST'

class ArticleSerializer(serializers.ModelSerializer):
    author = JournalistSerializer()
    publisher = PublisherSerializer(allow_null=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'author', 'publisher']
