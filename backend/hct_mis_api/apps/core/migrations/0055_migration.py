# Generated by Django 3.2.15 on 2022-09-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagefile',
            name='file',
            field=models.FileField(upload_to='files'),
        ),
    ]
