# Generated by Django 3.2.15 on 2022-12-06 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('power_query', '0005_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='hash',
            field=models.CharField(editable=False, max_length=200, unique=True),
        ),
    ]
