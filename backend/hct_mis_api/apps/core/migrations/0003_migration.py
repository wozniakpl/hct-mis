# Generated by Django 2.2.8 on 2020-07-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessarea',
            name='rapid_pro_api_key',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='rapid_pro_host',
            field=models.URLField(null=True),
        ),
    ]
