# Generated by Django 3.2.13 on 2022-08-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0077_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diiahousehold',
            name='status',
            field=models.CharField(blank=True, choices=[(None, 'To import'), ('IMPORTED', 'Imported'), ('ERROR', 'Error'), ('TAX_ID_ERROR', 'Tax ID Error')], max_length=16, null=True),
        ),
    ]
