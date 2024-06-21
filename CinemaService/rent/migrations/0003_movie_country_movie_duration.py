# Generated by Django 5.0.4 on 2024-06-20 11:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0002_alter_seat_booked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.TextField(default=django.utils.timezone.now, max_length=100, verbose_name='Страна'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.TextField(default=django.utils.timezone.now, max_length=30, verbose_name='Длительность'),
            preserve_default=False,
        ),
    ]
