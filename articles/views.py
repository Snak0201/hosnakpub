from django.views.generic import TemplateView, ListView
from .models import Article


# Create your views here.
class IndexView(TemplateView):
    template_name = "articles/index.html"

class ArticleListView(ListView):
    queryset = Article.objects.filter(is_published=True).order_by("-updated_at")
    template_name = "articles/list.html"
    context_object_name = "articles"
