# Generated by Django 3.2.22 on 2023-11-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0040_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='program',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='program',
            constraint=models.UniqueConstraint(condition=models.Q(('is_removed', False)), fields=('name', 'business_area', 'is_removed'), name='unique_for_program_if_not_removed'),
        ),
    ]
