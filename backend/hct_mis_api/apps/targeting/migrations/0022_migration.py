# Generated by Django 2.2.16 on 2021-10-07 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0021_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetpopulation',
            name='exclusion_reason',
            field=models.TextField(blank=True),
        ),
    ]
