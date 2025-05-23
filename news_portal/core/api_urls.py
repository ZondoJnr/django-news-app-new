from django.urls import path
from . import api_views

urlpatterns = [
    path('journalist/<int:journalist_id>/articles/', api_views.articles_by_journalist, name='api_articles_by_journalist'),
    path('publisher/<int:publisher_id>/articles/', api_views.articles_by_publisher, name='api_articles_by_publisher'),
]
