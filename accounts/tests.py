from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class IndexViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('accounts:index'))

    def test_get_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/index.html")
    
    def test_exist_right_title(self):
        self.assertContains(self.response, "<title>ほしのなか政府</title>", 1)
    
    def test_exist_favicon(self):
        self.assertContains(self.response, "favicon.ico", 1)
    
    def test_exist_navigation_bar(self):
        self.assertContains(self.response, "<nav>", 1)
    
    def test_exist_new_articles_space(self):
        self.assertContains(self.response, "最新記事", 1)
    
    def test_exist_bureaus_list_space(self):
        self.assertContains(self.response, "局一覧", 1)
    
    def test_exist_parilament_space(self):
        self.assertContains(self.response, "全民議会構成", 1)
    
    def test_exist_footer(self):
        self.assertContains(self.response, "<footer>", 1)
    
    def test_exist_credit(self):
        self.assertContains(self.response, "🄫 2023 Hoshinonaka/Snak", 1)
    
    def test_exist_logo_pictures(self):
        self.assertContains(self.response, "logo.png", 2)
    