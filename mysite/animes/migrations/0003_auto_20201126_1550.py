# Generated by Django 3.2 on 2020-11-26 15:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('animes', '0002_auto_20201126_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='animework',
            name='anime_airing_end_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animework',
            name='anime_airing_start_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
