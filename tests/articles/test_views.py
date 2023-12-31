from datetime import timedelta

import factory
import freezegun
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau


# Create your tests here.
class IndexViewTest(TestCase):
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
