from django.test import TestCase
from django.urls import reverse
from core.models import User, Article, Publisher

class ApproveArticleViewTest(TestCase):
    def setUp(self):
        self.editor = User.objects.create_user(username='editor', password='editorpass', role='EDITOR')
        self.reader = User.objects.create_user(username='reader', password='readerpass', role='READER', email='reader@example.com')
        self.journalist = User.objects.create_user(username='journalist', password='journalistpass', role='JOURNALIST')

        self.publisher = Publisher.objects.create(name='Daily News')
        self.publisher.editors.add(self.editor)
        self.reader.subscriptions_to_publishers.add(self.publisher)

        self.article = Article.objects.create(
            title='Breaking News',
            body='Important content',
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

    def test_approve_article_sets_approved_true(self):
        self.client.login(username='editor', password='editorpass')
        response = self.client.get(reverse('approve_article', args=[self.article.id]))
        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)
        self.assertEqual(response.status_code, 302)


class DashboardRedirectTest(TestCase):
    def test_redirects_to_correct_dashboard(self):
        roles = {
            'JOURNALIST': 'journalist_dashboard',
            'EDITOR': 'editor_dashboard',
            'READER': 'reader_dashboard',
            'PUBLISHER': 'publisher_dashboard'
        }
        for role, view in roles.items():
            user = User.objects.create_user(username=role.lower(), password='pass', role=role)
            self.client.login(username=role.lower(), password='pass')
            response = self.client.get(reverse('dashboard'))
            self.assertRedirects(response, reverse(view))
