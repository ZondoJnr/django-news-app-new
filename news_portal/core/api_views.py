# core/api_views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Article, User, Publisher
from .serializers import ArticleSerializer
from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])  # You can customize to Token/Auth based
def articles_by_journalist(request, journalist_id):
    journalist = User.objects.filter(id=journalist_id, role='JOURNALIST').first()
    if not journalist:
        return Response({"detail": "Journalist not found."}, status=404)

    articles = Article.objects.filter(author=journalist).order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def articles_by_publisher(request, publisher_id):
    publisher = Publisher.objects.filter(id=publisher_id).first()
    if not publisher:
        return Response({"detail": "Publisher not found."}, status=404)

    articles = Article.objects.filter(publisher=publisher).order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)
