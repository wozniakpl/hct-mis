# Generated by Django 3.2.15 on 2022-12-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessarea',
            name='kobo_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
