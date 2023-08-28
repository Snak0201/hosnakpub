from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article

# Register your models here.
admin.site.register(Article, MarkdownxModelAdmin)
