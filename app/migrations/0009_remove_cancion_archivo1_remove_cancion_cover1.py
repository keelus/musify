# Generated by Django 5.1.3 on 2024-11-17 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_cancion_archivo_cancion_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancion',
            name='archivo1',
        ),
        migrations.RemoveField(
            model_name='cancion',
            name='cover1',
        ),
    ]
