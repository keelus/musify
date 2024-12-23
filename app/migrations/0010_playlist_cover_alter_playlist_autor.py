# Generated by Django 5.1.3 on 2024-12-08 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_cancion_archivo1_remove_cancion_cover1'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='cover',
            field=models.URLField(default='temp'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario'),
        ),
    ]
