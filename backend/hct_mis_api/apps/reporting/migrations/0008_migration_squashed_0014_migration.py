# Generated by Django 3.2.19 on 2023-06-11 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('reporting', '0008_migration'), ('reporting', '0009_migration'), ('reporting', '0010_migration'), ('reporting', '0011_migration'), ('reporting', '0012_migration'), ('reporting', '0013_migration'), ('reporting', '0014_migration')]

    dependencies = [
        ('reporting', '0007_migration'),
        ('geo', '0004_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardreport',
            name='year',
            field=models.PositiveSmallIntegerField(default=2022),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.IntegerField(choices=[(1, 'Individuals'), (2, 'Households'), (3, 'Cash Plan Verification'), (4, 'Payments'), (5, 'Payment verification'), (6, 'Cash Plan'), (7, 'Programme'), (8, 'Individuals & Payment'), (9, 'Grievances')]),
        ),
        migrations.RemoveField(
            model_name='dashboardreport',
            name='admin_area',
        ),
        migrations.AddField(
            model_name='dashboardreport',
            name='admin_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_reports', to='geo.area'),
        ),
        migrations.RemoveField(
            model_name='report',
            name='admin_area',
        ),
        migrations.AddField(
            model_name='report',
            name='admin_area',
            field=models.ManyToManyField(blank=True, related_name='reports', to='geo.Area'),
        ),
    ]
