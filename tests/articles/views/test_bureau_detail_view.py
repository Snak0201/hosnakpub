from datetime import timedelta

import factory
import freezegun
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau


# Create your tests here.
class BureauDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BureauFactory.create()
        ArticleFactory.create(bureau=Bureau.objects.first(), is_published=True)

    def setUp(self):
        self.bureau = Bureau.objects.first()
        self.response = self.client.get(
            reverse("articles:bureau", kwargs={"slug": self.bureau.slug})
        )
        self.article = Article.objects.filter(bureau=self.bureau).first()

    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/bureau.html")

    def test_has_title(self):
        self.assertContains(
            self.response,
            f"<title>{self.bureau.name} | ほしのなか政府</title>",
        )

    def test_has_bureau_element(self):
        local_updated_at = self.bureau.updated_at + timedelta(hours=9)
        self.assertContains(self.response, f'<div id="name">{self.bureau.name}</div>')
        self.assertContains(
            self.response,
            f'<div id="updated_at">更新日時: {local_updated_at.strftime("%Y/%m/%d %H:%M")}</div>',
        )
        self.assertContains(
            self.response, f'<div id="content">{self.bureau.get_content()}</div>'
        )
        self.assertContains(
            self.response, f'<div id="articles"><span class="title"><h2>局記事一覧</h2>'
        )
        self.assertContains(
            self.response, f'<div id="committees"><span class="title"><h2>委員会一覧</h2>'
        )

    def test_has_bureau_articles(self):
        self.assertEqual(
            self.response.context["articles"].count(),
            Article.objects.filter(bureau=self.bureau).count(),
        )

    def test_link_to_article_detail(self):
        self.assertContains(
            self.response,
            f'<a href="{reverse("articles:detail", kwargs={"article_id": self.article.id})}">{self.article.title}</a>',
        )

    def test_does_not_get_view_bureau_is_not_found(self):
        response = self.client.get(reverse("articles:bureau", kwargs={"slug": "99"}))
        self.assertEqual(response.status_code, 404)

    def test_does_not_have_link_to_draft_articles(self):
        ArticleFactory.create(bureau=self.bureau)
        response = self.client.get(
            reverse("articles:bureau", kwargs={"slug": self.bureau.slug})
        )
        self.assertEqual(
            self.response.context["articles"].count(),
            response.context["articles"].count(),
        )
