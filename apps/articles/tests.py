# Create your tests here.
from django.test import TestCase, Client
from apps.articles.models import Article
import datetime

class ArticleModelTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article',
            posted_by='Test User',
            created_at=datetime.datetime.now()
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.content, 'This is a test article')
        self.assertEqual(self.article.posted_by, 'Test User')

    def test_article_like_count(self):
        self.assertEqual(self.article.like_count, 0)
        self.article.like_count += 1
        self.article.save()
        self.assertEqual(self.article.like_count, 1)

    def test_article_comment_count(self):
        self.assertEqual(self.article.comment_count, 0)
        self.article.comment_count += 1
        self.article.save()
        self.assertEqual(self.article.comment_count, 1)

    def test_articles_main_exist(self):
        response = Client().get("/articles/")
        self.assertEqual(response.status_code, 200)
    
    def test_articles_main_using_template(self):
        response = Client().get("/articles/")
        self.assertTemplateUsed(response, "article_main.html")

    def test_article_exist(self):
        response = Client().get(f"/articles/{self.article.id}/")
        self.assertEqual(response.status_code, 200)

    def test_articles_main_using_template(self):
        response = Client().get(f"/articles/{self.article.id}/")
        self.assertTemplateUsed(response, "article.html")