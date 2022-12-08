# Generated by Django 3.2.13 on 2022-08-16 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0059_migration"),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION payment_plan_business_area_seq() RETURNS trigger 
                LANGUAGE plpgsql
                AS $$
            begin
                execute format('create sequence if not exists payment_plan_business_area_seq_%s', translate(NEW.id::text, '-','_'));
                return NEW;
            end
            $$;

            """
        ),
        migrations.RunSQL(
            "CREATE TRIGGER payment_plan_business_area_seq AFTER INSERT ON core_businessarea FOR EACH ROW EXECUTE PROCEDURE payment_plan_business_area_seq();"
        ),
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION payment_business_area_seq() RETURNS trigger 
                LANGUAGE plpgsql
                AS $$
            begin
                execute format('create sequence if not exists payment_business_area_seq_%s', translate(NEW.id::text, '-','_'));
                return NEW;
            end
            $$;

            """
        ),
        migrations.RunSQL(
            "CREATE TRIGGER payment_business_area_seq AFTER INSERT ON core_businessarea FOR EACH ROW EXECUTE PROCEDURE payment_business_area_seq();"
        ),
    ]
