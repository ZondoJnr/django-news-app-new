from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import User, Article, Publisher

class SubscribedArticlesAPITest(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username='reader', password='readerpass', role='READER')
        self.journalist = User.objects.create_user(username='journalist', password='journalistpass', role='JOURNALIST')
        self.publisher = Publisher.objects.create(name='TechPress')
        self.publisher.editors.add(self.journalist)

        self.reader.subscriptions_to_journalists.add(self.journalist)

        self.article = Article.objects.create(
            title='AI in 2025',
            body='Future of artificial intelligence.',
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        self.client = APIClient()

    def test_subscribed_articles_returns_data(self):
        self.client.login(username='reader', password='readerpass')
        response = self.client.get(reverse('subscribed_articles'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'AI in 2025')

    def test_subscribed_articles_rejects_non_readers(self):
        self.client.login(username='journalist', password='journalistpass')
        response = self.client.get(reverse('subscribed_articles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
