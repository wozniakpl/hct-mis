# Generated by Django 2.2.8 on 2020-04-29 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0001_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetingcriteriarulefilter',
            name='field_name',
            field=models.CharField(max_length=50),
        ),
    ]
