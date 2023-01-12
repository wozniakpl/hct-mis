# Generated by Django 3.2.15 on 2023-01-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0007_migration'),
        ('household', '0134_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='admin1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='geo.area'),
        ),
        migrations.AddField(
            model_name='household',
            name='admin2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='geo.area'),
        ),
        migrations.AddField(
            model_name='household',
            name='admin3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='geo.area'),
        ),
        migrations.AddField(
            model_name='household',
            name='admin4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='geo.area'),
        ),
    ]
