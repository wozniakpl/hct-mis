# Generated by Django 3.2.15 on 2022-09-24 17:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import hct_mis_api.apps.account.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_migration'),
        ('api', '0001_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitoken',
            name='grants',
            field=hct_mis_api.apps.account.models.ChoiceArrayField(base_field=models.CharField(choices=[('API_READ_ONLY', 'API_READ_ONLY'), ('API_UPLOAD_RDI', 'API_UPLOAD_RDI'), ('API_CREATE_RDI', 'API_CREATE_RDI')], max_length=255), default=['API_READ_ONLY'], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apitoken',
            name='valid_for',
            field=models.ManyToManyField(to='core.BusinessArea'),
        ),
        migrations.CreateModel(
            name='APILogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.URLField()),
                ('method', models.CharField(max_length=10)),
                ('status_code', models.IntegerField()),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.apitoken')),
            ],
        ),
    ]
