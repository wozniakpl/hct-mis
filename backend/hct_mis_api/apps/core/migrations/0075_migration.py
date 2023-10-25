# Generated by Django 3.2.22 on 2023-10-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacollectingtype',
            name='deprecated',
            field=models.BooleanField(default=False, help_text='Cannot be used in new programs, totally hidden in UI, only admin have access'),
        ),
        migrations.AddField(
            model_name='datacollectingtype',
            name='type',
            field=models.CharField(blank=True, choices=[('STANDARD', 'Standard'), ('SOCIAL', 'Social Workers')], max_length=32, null=True),
        ),
    ]
