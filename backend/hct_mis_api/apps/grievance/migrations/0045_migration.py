# Generated by Django 3.2.13 on 2022-07-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0044_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grievanceticket',
            name='unicef_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
