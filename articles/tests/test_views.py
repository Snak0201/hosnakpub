from django.test import TestCase
from django.urls import reverse
from articles.models import Article

# Create your tests here.
class IndexViewTest(TestCase):
    fixtures = ["articles.json"]

    def setUp(self):
        self.response = self.client.get(reverse("articles:index"))

    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/index.html")

    def test_has_right_title(self):
        self.assertContains(self.response, "<title>ほしのなか政府</title>", 1)

    def test_has_favicon(self):
        self.assertContains(self.response, "favicon.ico", 1)

    def test_has_navigation_bar(self):
        self.assertContains(self.response, "<nav>", 1)

    def test_has_new_articles_space(self):
        self.assertContains(self.response, "最新記事", 1)
        self.assertEqual(self.response.context["articles"].count(), 5)

    def test_has_bureaus_list_space(self):
        self.assertContains(self.response, "局一覧", 1)

    def test_has_parilament_space(self):
        self.assertContains(self.response, "全民議会構成", 1)

    def test_has_footer(self):
        self.assertContains(self.response, "<footer>", 1)

    def test_has_credit(self):
        self.assertContains(self.response, "🄫 2023 Hoshinonaka/Snak", 1)

    def test_has_logo_pictures(self):
        self.assertContains(self.response, "logo.png", 2)
    
    def test_has_link_to_article_list(self):
        self.assertContains(self.response, f"href={reverse('articles:list')}")


class ArticleListViewTest(TestCase):
    fixtures = ["articles.json"]

    def setUp(self):
        self.response = self.client.get(reverse("articles:list"))
    
    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "articles/list.html")

    def test_has_right_title(self):
        self.assertContains(self.response, "記事一覧 | ほしのなか政府")      
      
    def test_has_all_published_articles_in_order_of_new_updated(self):
        self.assertEqual(self.response.context["articles"].count(), Article.objects.filter(is_published=True).count())
        self.assertQuerysetEqual(self.response.context["articles"], Article.objects.filter(is_published=True).order_by("-updated_at"))
