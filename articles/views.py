from typing import Any, Dict

from django.db import models
from django.views import generic

from .models import Article, Bureau


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_articles"] = Article.objects.filter(is_published=True).order_by(
            "-updated_at"
        )[:5]
        context["bureaus"] = Bureau.objects.all()
        return context


class ArticleListView(generic.ListView):
    queryset = Article.objects.filter(is_published=True).order_by("-updated_at")
    template_name = "articles/list.html"
    context_object_name = "articles"


class ArticleDetailView(generic.DetailView):
    template_name = "articles/detail.html"
    pk_url_kwarg = "article_id"
    context_object_name = "article"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_published=True)


class BureauDetailView(generic.DetailView):
    template_name = "articles/bureau.html"
    context_object_name = "bureau"
    model = Bureau

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(
            bureau=context["bureau"], is_published=True
        )
        return context
