# Generated by Django 3.2.18 on 2023-04-05 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0092_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedhousehold',
            name='zip_code',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
