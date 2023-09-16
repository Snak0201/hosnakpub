from factory.django import DjangoModelFactory

from .models import Article, Bureau


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = "テスト記事"
    content_with_markdown = "テスト用記事"
    is_published = False


class BureauFactory(DjangoModelFactory):
    class Meta:
        model = Bureau

    name = "テスト局"
    slug = "test"
    content_with_markdown = "テスト用の局です。"
