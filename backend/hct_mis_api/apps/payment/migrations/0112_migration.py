# Generated by Django 3.2.22 on 2023-11-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0111_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='signature_hash',
            field=models.CharField(blank=True, editable=False, max_length=40),
        ),
    ]
