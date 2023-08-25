from django.db import models
from markdownx.models import MarkdownxField


# Create your models here.
class Article(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=255)
    content = MarkdownxField(verbose_name="内容")
    is_published = models.BooleanField(verbose_name="公開", default=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="最終更新日時", auto_now=True)
