from datetime import timedelta

import factory
import freezegun
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau
from tests.utils import E2ETestCase
from selenium.webdriver.common.by import By


class IndexViewUnitTest(TestCase):
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
        BureauFactory.create_batch(
            5,
            name=factory.Sequence(lambda n: f"テスト局{n}"),
            slug=factory.Sequence(lambda n: f"test{n}"),
        )
        cls.article_update()

    def setUp(self):
        self.response = self.client.get(reverse("articles:index"))
        self.newest_article = (
            Article.objects.filter(is_published=True).order_by("-updated_at").first()
        )
        self.bureau = Bureau.objects.first()

    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/index.html")

    def test_has_title(self):
        self.assertContains(self.response, "favicon.ico", 1)
        self.assertContains(self.response, "<title>ほしのなか政府</title>", 1)

    def test_has_description(self):
        self.assertRegex(
            self.response.content.decode(), r'<meta name="description" content=.+>'
        )

    def test_has_header_navigation_bar(self):
        self.assertContains(self.response, "<nav>", 1)
        self.assertContains(
            self.response,
            f'<a class="navItem" href="{reverse("articles:list")}">記事一覧</a>',
        )

    def test_has_five_published_articles_in_order_of_new_updated(self):
        self.assertContains(self.response, "最新記事", 1)
        self.assertEqual(self.response.context["new_articles"].count(), 5)
        self.assertQuerysetEqual(
            self.response.context["new_articles"],
            Article.objects.filter(is_published=True).order_by("-updated_at")[:5],
        )

    def test_has_link_to_article_detail(self):
        self.assertContains(
            self.response,
            f'<a href="{reverse("articles:detail", kwargs={"article_id": self.newest_article.id})}">{self.newest_article.title}</a>',
        )
        self.assertContains(
            self.response,
            f'<a href="{reverse("articles:detail", kwargs={"article_id": 1})}">',
        )

    def test_has_link_to_article_list(self):
        self.assertContains(
            self.response, f'<a href="{reverse("articles:list")}">記事一覧へ</a>'
        )

    def test_has_bureaus_list(self):
        self.assertContains(self.response, "局一覧", 1)
        self.assertEqual(
            self.response.context["bureaus"].count(), Bureau.objects.all().count()
        )

    def test_has_link_to_bureau_detail(self):
        self.assertContains(
            self.response,
            f'<a href="{reverse("articles:bureau", kwargs={"slug": self.bureau.slug})}">{self.bureau.name}</a>',
        )

    def test_has_parilament_space(self):
        self.assertContains(self.response, "全民議会構成", 1)

    def test_has_footer(self):
        self.assertContains(self.response, "<footer>", 1)
        self.assertContains(self.response, "©️ 2023 Hoshinonaka/Snak", 1)

    def test_has_logo_pictures(self):
        self.assertContains(self.response, "logo.png", 2)
        

class IndexViewE2ETest(E2ETestCase):
    def test_get_view(self):
        self.selenium.get(self.live_server_url)
        self.assertEqual("ほしのなか政府", self.selenium.title)
        print(self.selenium.find_element(By.TAG_NAME, "a").text)
