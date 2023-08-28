from typing import Any, Dict

from django.views import generic

from .models import Article


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["new_articles"] = Article.objects.filter(is_published=True).order_by(
            "-updated_at"
        )[:5]
        return context


class ArticleListView(generic.ListView):
    queryset = Article.objects.filter(is_published=True).order_by("-updated_at")
    template_name = "articles/list.html"
    context_object_name = "articles"

class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = "articles/detail.html"
    pk_url_kwarg = "article_id"
    context_object_name = "article"