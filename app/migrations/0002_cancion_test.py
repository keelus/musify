# Generated by Django 5.1.3 on 2024-11-14 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancion',
            name='test',
            field=models.FileField(default='hola', upload_to=''),
            preserve_default=False,
        ),
    ]