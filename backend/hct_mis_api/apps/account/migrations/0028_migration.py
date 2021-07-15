# Generated by Django 2.2.16 on 2021-07-13 08:15

import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_migration'),
        ('steficon', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=100, unique=True)),
                ('is_un', models.BooleanField(default=False, verbose_name='U.N.')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='account.Partner'),
        ),
    ]
