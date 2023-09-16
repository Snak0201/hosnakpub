import bleach
from bleach_allowlist import markdown_attrs, markdown_tags
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class Article(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=255)
    content_with_markdown = MarkdownxField(verbose_name="内容のマークダウン記述")
    is_published = models.BooleanField(verbose_name="公開", default=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="最終更新日時", auto_now=True)

    def get_content(self):
        raw_html = markdownify(self.content_with_markdown)
        markdown_attrs["*"] = ["class", "id"]
        markdown_attrs["img"] = ["src", "alt", "title", "width", "height"]
        return bleach.clean(raw_html, tags=markdown_tags, attributes=markdown_attrs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "記事"
        verbose_name_plural = "記事"


class Bureau(models.Model):
    name = models.CharField(verbose_name="局名", max_length=10)
    slug = models.SlugField(verbose_name="slug")
    content_with_markdown = MarkdownxField(verbose_name="局紹介文のマークダウン記述")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="最終更新日時", auto_now=True)

    def get_content(self):
        raw_html = markdownify(self.content_with_markdown)
        markdown_attrs["*"] = ["class", "id"]
        markdown_attrs["img"] = ["src", "alt", "title", "width", "height"]
        return bleach.clean(raw_html, tags=markdown_tags, attributes=markdown_attrs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "局"
        verbose_name_plural = "局"
