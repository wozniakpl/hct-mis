# Generated by Django 3.2.15 on 2023-01-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0086_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedhousehold',
            name='admin3',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='admin3_title',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='admin4',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='admin4_title',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='admin_area',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='admin_area_title',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
