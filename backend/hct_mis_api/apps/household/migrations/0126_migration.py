# Generated by Django 3.2.15 on 2022-10-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0125_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
