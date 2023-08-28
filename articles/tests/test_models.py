from django.test import TestCase
from django.db import transaction, IntegrityError
from articles.models import Article
import freezegun
from datetime import datetime, timezone

class ArticleModelTest(TestCase):
    @freezegun.freeze_time("2023-02-01 00:00:00")
    def setUp(self):
        self.article = Article.objects.create(title="テスト記事", content="テスト記事", is_published=True)
        
    @freezegun.freeze_time("2023-02-01 00:00:00")
    def test_create_article(self):
        self.assertEqual(datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.created_at)
        self.assertEqual(datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.updated_at)
    
    @freezegun.freeze_time("2023-02-01 12:34:56")
    def test_update_article(self):
        self.article.content = "テスト記事2"
        self.article.save()
        self.assertEqual(datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.created_at)
        self.assertEqual(datetime(2023, 2, 1, 12, 34, 56, tzinfo=timezone.utc), self.article.updated_at)
    
    def test_invalid_no_title_article(self):
        articles_count = Article.objects.all().count()
        article = Article(title=None, content="テスト記事")
        try:
            with transaction.atomic():
                article.save()
        except IntegrityError:
            pass
        self.assertEqual(articles_count, Article.objects.all().count())

    def test_invalid_no_content_article(self):
        articles_count = Article.objects.all().count()
        article = Article(title="テスト記事", content=None)
        try:
            with transaction.atomic():
                article.save()
        except IntegrityError:
            pass
        self.assertEqual(articles_count, Article.objects.all().count())
