from datetime import timedelta

import factory
import freezegun
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau


class ArticleDetailViewTest(TestCase):
    @classmethod
    @freezegun.freeze_time("2023-02-01 01:23:45")
    def setUpTestData(cls):
        BureauFactory.create()
        ArticleFactory.create_batch(
            5,
            title=factory.Sequence(lambda n: f"公開記事{n}"),
            is_published=True,
            bureau=Bureau.objects.first(),
        )
        ArticleFactory.create_batch(3, title=factory.Sequence(lambda n: f"非公開記事{n}"))
        get_user_model().objects.create_user(
            username="Test Staff", password="password", is_staff=True
        )

    @freezegun.freeze_time("2023-02-01 12:34:56")
    def setUp(self):
        new_article = Article.objects.first()
        new_article.content = "NEW"
        new_article.save()
        self.published_article = Article.objects.filter(is_published=True).first()
        self.draft_article = Article.objects.filter(is_published=False).first()
        self.response_published = self.client.get(
            reverse("articles:detail", kwargs={"article_id": self.published_article.id})
        )
        self.response_draft = self.client.get(
            reverse("articles:detail", kwargs={"article_id": self.draft_article.id})
        )
        self.staff = get_user_model().objects.get(username="Test Staff")
        self.client.force_login(self.staff)
        self.response_draft_with_staff = self.client.get(
            reverse("articles:detail", kwargs={"article_id": self.draft_article.id})
        )

    def test_get_view_published(self):
        self.assertEqual(self.response_published.status_code, 200)
        self.assertTemplateUsed("articles/detail.html")

    def test_has_right_title_published(self):
        self.assertContains(
            self.response_published,
            f"<title>{self.published_article.title} | ほしのなか政府</title>",
        )

    def test_has_article_element(self):
        local_updated_at = self.published_article.updated_at + timedelta(hours=9)
        self.assertContains(
            self.response_published,
            f'<div id="title">{self.published_article.title}</div>',
        )
        self.assertContains(
            self.response_published,
            f'<div id="content">{self.published_article.get_content()}</div>',
        )

        self.assertContains(
            self.response_published,
            f'<div id="updated_at">更新日時: {local_updated_at.strftime("%Y/%m/%d %H:%M")}</div>',
        )
        self.assertContains(
            self.response_published,
            f'<a href="{reverse("articles:bureau", kwargs={"slug": self.published_article.bureau.slug})}">{self.published_article.bureau.name}',
        )
        self.assertContains(
            self.response_published, f'<a href="{reverse("articles:list")}">記事一覧へ</a>'
        )

    def test_does_not_get_view_article_is_not_found(self):
        response = self.client.get(
            reverse("articles:detail", kwargs={"article_id": 99})
        )
        self.assertEqual(response.status_code, 404)

    def test_does_not_get_view_draft_without_login(self):
        self.assertEqual(self.response_draft.status_code, 404)

    def test_get_view_draft_with_staff(self):
        self.assertEqual(self.response_draft_with_staff.status_code, 200)

    def test_has_draft_mark_draft_with_staff(self):
        self.assertContains(self.response_draft_with_staff, "下書き", 2)

    def test_has_right_title_draft_with_staff(self):
        self.assertContains(
            self.response_draft_with_staff,
            f"<title>（下書き）{self.draft_article.title} | ほしのなか政府</title>",
        )
