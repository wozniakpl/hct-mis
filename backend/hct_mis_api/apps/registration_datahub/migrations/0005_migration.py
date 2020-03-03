# Generated by Django 2.2.8 on 2020-02-28 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0004_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationdataimportdatahub',
            name='data_source',
        ),
        migrations.RemoveField(
            model_name='registrationdataimportdatahub',
            name='imported_by',
        ),
        migrations.RemoveField(
            model_name='registrationdataimportdatahub',
            name='status',
        ),
        migrations.AddField(
            model_name='registrationdataimportdatahub',
            name='hct_id',
            field=models.UUIDField(null=True, default=None),
        ),
    ]
