# Generated by Django 4.2 on 2023-08-30 05:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0004_alter_article_is_published"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="content",
            new_name="content_with_markdown",
        ),
    ]
