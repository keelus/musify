# Generated by Django 5.1.3 on 2024-11-14 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cancion_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancion',
            name='test',
        ),
        migrations.AlterField(
            model_name='cancion',
            name='archivo',
            field=models.FileField(upload_to=''),
        ),
    ]
