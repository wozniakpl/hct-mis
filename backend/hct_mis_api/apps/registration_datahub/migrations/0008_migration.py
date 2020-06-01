# Generated by Django 2.2.8 on 2020-05-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0007_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importdata',
            old_name='xlsx_file',
            new_name='file',
        ),
        migrations.AddField(
            model_name='importdata',
            name='data_type',
            field=models.CharField(choices=[('XLSX', 'XLSX File'), ('JSON', 'JSON File')], default='XLSX', max_length=4),
        ),
    ]
