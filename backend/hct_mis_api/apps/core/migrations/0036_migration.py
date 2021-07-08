# Generated by Django 2.2.16 on 2021-07-08 09:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_golden_record_min_score',
            field=models.DecimalField(decimal_places=1, default=6.0, help_text='Results below the minimum score will not be taken into account', max_digits=3, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
