# Generated by Django 2.2.16 on 2021-01-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_log', '0001_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='object_repr',
            field=models.TextField(blank=True),
        ),
    ]
