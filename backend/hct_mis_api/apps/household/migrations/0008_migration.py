# Generated by Django 2.2.8 on 2020-06-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0007_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='administration_of_rutf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='individual',
            name='enrolled_in_nutrition_programme',
            field=models.BooleanField(default=False),
        ),
    ]
