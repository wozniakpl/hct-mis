# Generated by Django 2.2.16 on 2021-06-24 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0027_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='grievanceticket',
            name='unicef_id',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
