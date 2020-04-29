# Generated by Django 2.2.8 on 2020-04-29 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('household', '0002_migration'),
        ('payment', '0001_migration'),
        ('program', '0001_migration'),
        ('targeting', '0001_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='cash_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='program.CashPlan'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='entitlement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_record', to='payment.PaymentEntitlement'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='household.Household'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='payment_record_verification',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.PaymentRecordVerification'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='target_population',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_records', to='targeting.TargetPopulation'),
        ),
    ]
