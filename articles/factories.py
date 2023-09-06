import factory
from factory.django import DjangoModelFactory
from .models import Article

class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article
    
    title = "テスト記事"
    content_with_markdown = "テスト用記事"
    is_published = False
    
    

    
