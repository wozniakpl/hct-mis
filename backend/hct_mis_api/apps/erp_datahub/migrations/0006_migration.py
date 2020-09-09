# Generated by Django 2.2.8 on 2020-09-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp_datahub', '0005_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='business_area',
            field=models.CharField(default='0060', help_text='Same as the business area set on program, but\n            this is set as the same value, and all other\n            models this way can get easy access to the business area\n            via the session.', max_length=20),
            preserve_default=False,
        ),
    ]
