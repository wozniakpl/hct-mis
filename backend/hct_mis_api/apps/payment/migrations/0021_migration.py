# Generated by Django 2.2.16 on 2021-02-12 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0052_migration'),
        ('payment', '0020_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='head_of_household',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='household.Individual'),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='delivery_type',
            field=models.CharField(choices=[('CASH', 'Cash'), ('DEPOSIT_TO_CARD', 'Deposit to Card'), ('TRANSFER', 'Transfer')], max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='entitlement_card_issue_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='entitlement_card_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='entitlement_card_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='status',
            field=models.CharField(choices=[('SUCCESS', 'Success'), ('PENDING', 'Pending'), ('ERROR', 'Error')], max_length=255),
        ),
    ]
