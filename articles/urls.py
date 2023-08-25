from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("articles/", views.ArticleListView.as_view(), name="list"),
]