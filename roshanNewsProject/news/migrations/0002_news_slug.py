# Generated by Django 5.2.4 on 2025-07-12 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
