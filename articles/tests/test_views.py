from django.test import TestCase
from django.urls import reverse
from articles.models import Article

class ArticleListViewTest(TestCase):
    fixtures = ["articles.json"]

    def setUp(self):
        self.response = self.client.get(reverse("articles:list"))
    
    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/list.html")      
    
    def test_has_all_published_articles(self):
        self.assertEqual(self.response.context["articles"].count(), Article.objects.filter(is_draft=False).count())  

    def test_articles_are_in_order_of_new_updated(self):
        pass


class ArticleDetailViewTest(TestCase):
    fixtures = ["articles.json"]

    def setUp(self):
        self.response_not_draft = self.client.get(reverse("articles:detail", kwargs={"pk": 1}))
        self.article_not_draft = Article.objects.filter(is_draft=False)
    
    def test_get_view_not_draft(self):
        self.assertEqual(self.response_not_draft.status_code, 200)
        self.assertTemplateUsed(self.response_not_draft, "articles/detail.html")
        self.assertEqual(self.response_not_draft.context["article"], self.article_not_draft)