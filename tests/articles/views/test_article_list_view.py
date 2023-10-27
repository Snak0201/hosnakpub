from datetime import timedelta

import factory
import freezegun
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau


class ArticleListViewTest(TestCase):
    @freezegun.freeze_time("2023-02-01 12:34:56")
    def article_update():
        new_article = Article.objects.first()
        new_article.content = "NEW"
        new_article.save()

    @classmethod
    @freezegun.freeze_time("2023-02-01 01:23:45")
    def setUpTestData(cls):
        ArticleFactory.create_batch(
            7, title=factory.Sequence(lambda n: f"公開記事{n}"), is_published=True
        )
        ArticleFactory.create_batch(3, title=factory.Sequence(lambda n: f"非公開記事{n}"))
        cls.article_update()

    @freezegun.freeze_time("2023-02-01 12:34:56")
    def setUp(self):
        self.response = self.client.get(reverse("articles:list"))
        self.newest_article = (
            Article.objects.filter(is_published=True).order_by("-updated_at").first()
        )

    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/list.html")

    def test_has_right_title(self):
        self.assertContains(self.response, "記事一覧 | ほしのなか政府")

    def test_has_all_published_articles_in_order_of_new_updated(self):
        self.assertEqual(
            self.response.context["articles"].count(),
            Article.objects.filter(is_published=True).count(),
        )
        self.assertQuerysetEqual(
            self.response.context["articles"],
            Article.objects.filter(is_published=True).order_by("-updated_at"),
        )

    def test_has_link_to_article_detail(self):
        self.assertContains(
            self.response,
            f'<a href="{reverse("articles:detail", kwargs={"article_id": self.newest_article.id})}">{self.newest_article.title}</a>',
        )
