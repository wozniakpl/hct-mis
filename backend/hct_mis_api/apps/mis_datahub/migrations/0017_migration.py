# Generated by Django 2.2.8 on 2020-08-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_datahub', '0016_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='household_mis_id',
            field=models.UUIDField(null=True),
        ),
    ]
