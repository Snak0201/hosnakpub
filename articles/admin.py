from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article, Bureau

# Register your models here.
admin.site.register(Article, MarkdownxModelAdmin)
admin.site.register(Bureau)
