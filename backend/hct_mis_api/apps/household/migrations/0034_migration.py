# Generated by Django 2.2.8 on 2020-04-28 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0033_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='identity',
            unique_together={('agency', 'number')},
        ),
    ]
