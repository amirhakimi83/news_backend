# Generated by Django 5.2.4 on 2025-07-12 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='slug',
        ),
    ]
