# Generated by Django 4.2 on 2023-08-25 03:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0002_alter_article_content"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="is_draft",
            new_name="is_published",
        ),
    ]
