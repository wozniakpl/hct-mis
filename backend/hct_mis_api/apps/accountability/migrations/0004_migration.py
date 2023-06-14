# Generated by Django 3.2.13 on 2022-10-05 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountability', '0003_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='issue_type',
            field=models.CharField(choices=[('POSITIVE_FEEDBACK', 'Positive feedback'), ('NEGATIVE_FEEDBACK', 'Negative feedback')], max_length=20, verbose_name='Issue type'),
        ),
    ]
