# Generated by Django 2.2.16 on 2021-02-23 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_migration_squashed_0029_migration'),
        ('program', '0024_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashplan',
            name='service_provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_plans', to='payment.ServiceProvider'),
        ),
    ]
