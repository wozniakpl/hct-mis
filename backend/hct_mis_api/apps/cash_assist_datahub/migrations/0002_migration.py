# Generated by Django 2.2.8 on 2020-06-18 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash_assist_datahub', '0001_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrecord',
            name='session',
        ),
        migrations.RemoveField(
            model_name='programme',
            name='session',
        ),
        migrations.RemoveField(
            model_name='serviceprovider',
            name='session',
        ),
        migrations.RemoveField(
            model_name='targetpopulation',
            name='session',
        ),
        migrations.DeleteModel(
            name='CashPlan',
        ),
        migrations.DeleteModel(
            name='PaymentRecord',
        ),
        migrations.DeleteModel(
            name='Programme',
        ),
        migrations.DeleteModel(
            name='ServiceProvider',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
        migrations.DeleteModel(
            name='TargetPopulation',
        ),
    ]
