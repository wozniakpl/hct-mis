# Generated by Django 2.2.8 on 2020-08-13 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0015_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='individualidentity',
            unique_together=set(),
        ),
    ]
