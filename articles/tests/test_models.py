from datetime import datetime, timezone

import freezegun
from django.db import DataError, IntegrityError, transaction
from django.test import TestCase

from articles.factories import ArticleFactory, BureauFactory
from articles.models import Article, Bureau


class ArticleModelTest(TestCase):
    @freezegun.freeze_time("2023-02-01 00:00:00")
    def setUp(self):
        self.article = ArticleFactory()
        self.articles_count = Article.objects.count()

    @freezegun.freeze_time("2023-02-01 00:00:00")
    def test_create_article(self):
        self.assertEqual(
            datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.created_at
        )
        self.assertEqual(
            datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.updated_at
        )

    @freezegun.freeze_time("2023-02-01 12:34:56")
    def test_update_article(self):
        self.article.content = "テスト記事2"
        self.article.save()
        self.assertEqual(
            datetime(2023, 2, 1, 0, 0, 0, tzinfo=timezone.utc), self.article.created_at
        )
        self.assertEqual(
            datetime(2023, 2, 1, 12, 34, 56, tzinfo=timezone.utc),
            self.article.updated_at,
        )

    def test_invalid_no_title_article(self):
        article = ArticleFactory.build(title=None)
        try:
            with transaction.atomic():
                article.save()
        except IntegrityError:
            pass
        self.assertEqual(self.articles_count, Article.objects.all().count())

    def test_invalid_no_content_article(self):
        article = ArticleFactory.build(content_with_markdown=None)
        try:
            with transaction.atomic():
                article.save()
        except IntegrityError:
            pass
        self.assertEqual(self.articles_count, Article.objects.all().count())

    def test_convert_content(self):
        article = ArticleFactory.build(content_with_markdown="## 見出し2")
        self.assertEqual(article.get_content(), "<h2>見出し2</h2>")
        article = ArticleFactory.build(
            content_with_markdown='<div class="ipIgawaAoi"></div>'
        )
        self.assertEqual(article.get_content(), '<div class="ipIgawaAoi"></div>')
        article = ArticleFactory.build(
            content_with_markdown="|head|head|\n|----|----|\n|value|value|"
        )
        self.assertEqual(
            article.get_content(),
            "<table>\n<thead>\n<tr>\n<th>head</th>\n<th>head</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>value</td>\n<td>value</td>\n</tr>\n</tbody>\n</table>",
        )

    def test_escape_script_tag_in_content(self):
        article = ArticleFactory.build(content_with_markdown="<script>main()</script>")
        self.assertNotEqual(article.get_content(), "<script>main()</script>")

    def test_valid_article_relates_bureau(self):
        BureauFactory.create()
        article = ArticleFactory.build(bureau=Bureau.objects.first())
        article.save()
        self.assertEqual(self.articles_count + 1, Article.objects.count())

    def test_valid_article_does_not_relate_bureau(self):
        article = ArticleFactory.build(bureau=None)
        article.save()
        self.assertEqual(self.articles_count + 1, Article.objects.count())


class BureauModelTest(TestCase):
    @freezegun.freeze_time("2023-02-01 01:23:45")
    def setUp(self):
        self.bureau = BureauFactory()
        self.bureaus_count = Bureau.objects.count()

    def test_create_bureau(self):
        self.assertEqual(
            datetime(2023, 2, 1, 1, 23, 45, tzinfo=timezone.utc), self.bureau.created_at
        )
        self.assertEqual(
            datetime(2023, 2, 1, 1, 23, 45, tzinfo=timezone.utc), self.bureau.updated_at
        )

    @freezegun.freeze_time("2023-02-01 12:34:56")
    def test_update_bureau(self):
        self.bureau.name = "テスト局（メンテ）"
        self.bureau.save()
        self.assertEqual(
            datetime(2023, 2, 1, 1, 23, 45, tzinfo=timezone.utc), self.bureau.created_at
        )
        self.assertEqual(
            datetime(2023, 2, 1, 12, 34, 56, tzinfo=timezone.utc),
            self.bureau.updated_at,
        )

    def test_invalid_too_long_name_bureau(self):
        bureau = BureauFactory.build(name="12345678901")
        try:
            with transaction.atomic():
                bureau.save()
        except DataError:
            pass
        self.assertEqual(self.bureaus_count, Bureau.objects.count())

    def test_convert_content(self):
        bureau = BureauFactory.build(content_with_markdown="## 見出し2")
        self.assertEqual(bureau.get_content(), "<h2>見出し2</h2>")
        bureau = BureauFactory.build(
            content_with_markdown="|head|head|\n|----|----|\n|value|value|"
        )
        self.assertEqual(
            bureau.get_content(),
            "<table>\n<thead>\n<tr>\n<th>head</th>\n<th>head</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>value</td>\n<td>value</td>\n</tr>\n</tbody>\n</table>",
        )
        bureau = BureauFactory.build(
            content_with_markdown='<div class="ipIgawaAoi"></div>'
        )
        self.assertEqual(bureau.get_content(), '<div class="ipIgawaAoi"></div>')

    def test_escape_script_tag_in_content(self):
        bureau = BureauFactory.build(content_with_markdown="<script>main()</script>")
        self.assertNotEqual(bureau.get_content(), "<script>main()</script>")
