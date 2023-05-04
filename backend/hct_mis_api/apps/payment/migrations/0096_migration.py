# Generated by Django 3.2.18 on 2023-04-24 12:36

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0095_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialserviceproviderxlsxtemplate',
            name='columns',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('payment_id', 'Payment ID'), ('household_id', 'Household ID'), ('household_size', 'Household Size'), ('collector_name', 'Collector Name'), ('payment_channel', 'Payment Channel'), ('fsp_name', 'FSP Name'), ('currency', 'Currency'), ('entitlement_quantity', 'Entitlement Quantity'), ('entitlement_quantity_usd', 'Entitlement Quantity USD'), ('delivered_quantity', 'Delivered Quantity'), ('delivery_date', 'Delivery date')], default=['payment_id', 'household_id', 'household_size', 'collector_name', 'payment_channel', 'fsp_name', 'currency', 'entitlement_quantity', 'entitlement_quantity_usd', 'delivered_quantity', 'delivery_date'], help_text='Select the columns to include in the report', max_length=166, verbose_name='Columns'),
        ),
    ]
