# Generated by Django 5.0.4 on 2024-06-20 11:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_movie_country_movie_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='composer',
            field=models.TextField(default=django.utils.timezone.now, max_length=300, verbose_name='Композитор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.TextField(default=django.utils.timezone.now, max_length=300, verbose_name='Режиссер'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='producer',
            field=models.TextField(default=django.utils.timezone.now, max_length=300, verbose_name='Продюсер'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='script',
            field=models.TextField(default=django.utils.timezone.now, max_length=300, verbose_name='Сценарий'),
            preserve_default=False,
        ),
    ]
