# Generated by Django 2.2.16 on 2020-12-15 19:23

import hct_mis_api.apps.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=hct_mis_api.apps.account.models.ChoiceArrayField(base_field=models.CharField(choices=[('RDI_VIEW_LIST', 'RDI VIEW LIST'), ('RDI_VIEW_DETAILS', 'RDI VIEW DETAILS'), ('RDI_IMPORT_DATA', 'RDI IMPORT DATA'), ('RDI_RERUN_DEDUPE', 'RDI RERUN DEDUPE'), ('RDI_MERGE_IMPORT', 'RDI MERGE IMPORT'), ('POPULATION_VIEW_HOUSEHOLDS_LIST', 'POPULATION VIEW HOUSEHOLDS LIST'), ('POPULATION_VIEW_HOUSEHOLDS_DETAILS', 'POPULATION VIEW HOUSEHOLDS DETAILS'), ('POPULATION_VIEW_INDIVIDUALS_LIST', 'POPULATION VIEW INDIVIDUALS LIST'), ('POPULATION_VIEW_INDIVIDUALS_DETAILS', 'POPULATION VIEW INDIVIDUALS DETAILS'), ('PRORGRAMME_VIEW_LIST_AND_DETAILS', 'PRORGRAMME VIEW LIST AND DETAILS'), ('PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS', 'PROGRAMME VIEW PAYMENT RECORD DETAILS'), ('PROGRAMME_CREATE', 'PROGRAMME CREATE'), ('PROGRAMME_UPDATE', 'PROGRAMME UPDATE'), ('PROGRAMME_REMOVE', 'PROGRAMME REMOVE'), ('PROGRAMME_ACTIVATE', 'PROGRAMME ACTIVATE'), ('PROGRAMME_FINISH', 'PROGRAMME FINISH'), ('TARGETING_VIEW_LIST', 'TARGETING VIEW LIST'), ('TARGETING_VIEW_DETAILS', 'TARGETING VIEW DETAILS'), ('TARGETING_CREATE', 'TARGETING CREATE'), ('TARGETING_UPDATE', 'TARGETING UPDATE'), ('TARGETING_DUPLICATE', 'TARGETING DUPLICATE'), ('TARGETING_REMOVE', 'TARGETING REMOVE'), ('TARGETING_LOCK', 'TARGETING LOCK'), ('TARGETING_UNLOCK', 'TARGETING UNLOCK'), ('TARGETING_SEND', 'TARGETING SEND'), ('PAYMENT_VERIFICATION_VIEW_LIST', 'PAYMENT VERIFICATION VIEW LIST'), ('PAYMENT_VERIFICATION_VIEW_DETAILS', 'PAYMENT VERIFICATION VIEW DETAILS'), ('PAYMENT_VERIFICATION_CREATE', 'PAYMENT VERIFICATION CREATE'), ('PAYMENT_VERIFICATION_UPDATE', 'PAYMENT VERIFICATION UPDATE'), ('PAYMENT_VERIFICATION_ACTIVATE', 'PAYMENT VERIFICATION ACTIVATE'), ('PAYMENT_VERIFICATION_DISCARD', 'PAYMENT VERIFICATION DISCARD'), ('PAYMENT_VERIFICATION_FINISH', 'PAYMENT VERIFICATION FINISH'), ('PAYMENT_VERIFICATION_EXPORT', 'PAYMENT VERIFICATION EXPORT'), ('PAYMENT_VERIFICATION_IMPORT', 'PAYMENT VERIFICATION IMPORT'), ('PAYMENT_VERIFICATION_VERIFY', 'PAYMENT VERIFICATION VERIFY'), ('PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS', 'PAYMENT VERIFICATION VIEW PAYMENT RECORD DETAILS'), ('USER_MANAGEMENT_VIEW_LIST', 'USER MANAGEMENT VIEW LIST'), ('DASHBOARD_VIEW_HQ', 'DASHBOARD VIEW HQ'), ('DASHBOARD_VIEW_COUNTRY', 'DASHBOARD VIEW COUNTRY'), ('DASHBOARD_EXPORT', 'DASHBOARD EXPORT'), ('GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE', 'GRIEVANCES VIEW LIST EXCLUDING SENSITIVE'), ('GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_CREATOR', 'GRIEVANCES VIEW LIST EXCLUDING SENSITIVE AS CREATOR'), ('GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_OWNER', 'GRIEVANCES VIEW LIST EXCLUDING SENSITIVE AS OWNER'), ('GRIEVANCES_VIEW_LIST_SENSITIVE', 'GRIEVANCES VIEW LIST SENSITIVE'), ('GRIEVANCES_VIEW_LIST_SENSITIVE_AS_CREATOR', 'GRIEVANCES VIEW LIST SENSITIVE AS CREATOR'), ('GRIEVANCES_VIEW_LIST_SENSITIVE_AS_OWNER', 'GRIEVANCES VIEW LIST SENSITIVE AS OWNER'), ('GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE', 'GRIEVANCES VIEW DETAILS EXCLUDING SENSITIVE'), ('GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_CREATOR', 'GRIEVANCES VIEW DETAILS EXCLUDING SENSITIVE AS CREATOR'), ('GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_OWNER', 'GRIEVANCES VIEW DETAILS EXCLUDING SENSITIVE AS OWNER'), ('GRIEVANCES_VIEW_DETAILS_SENSITIVE', 'GRIEVANCES VIEW DETAILS SENSITIVE'), ('GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_CREATOR', 'GRIEVANCES VIEW DETAILS SENSITIVE AS CREATOR'), ('GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_OWNER', 'GRIEVANCES VIEW DETAILS SENSITIVE AS OWNER'), ('GRIEVANCES_VIEW_HOUSEHOLD_DETAILS', 'GRIEVANCES VIEW HOUSEHOLD DETAILS'), ('GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_CREATOR', 'GRIEVANCES VIEW HOUSEHOLD DETAILS AS CREATOR'), ('GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_OWNER', 'GRIEVANCES VIEW HOUSEHOLD DETAILS AS OWNER'), ('GRIEVANCES_VIEW_INDIVIDUALS_DETAILS', 'GRIEVANCES VIEW INDIVIDUALS DETAILS'), ('GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_CREATOR', 'GRIEVANCES VIEW INDIVIDUALS DETAILS AS CREATOR'), ('GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_OWNER', 'GRIEVANCES VIEW INDIVIDUALS DETAILS AS OWNER'), ('GRIEVANCES_CREATE', 'GRIEVANCES CREATE'), ('GRIEVANCES_UPDATE', 'GRIEVANCES UPDATE'), ('GRIEVANCES_UPDATE_AS_CREATOR', 'GRIEVANCES UPDATE AS CREATOR'), ('GRIEVANCES_UPDATE_AS_OWNER', 'GRIEVANCES UPDATE AS OWNER'), ('GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE', 'GRIEVANCES UPDATE REQUESTED DATA CHANGE'), ('GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_CREATOR', 'GRIEVANCES UPDATE REQUESTED DATA CHANGE AS CREATOR'), ('GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_OWNER', 'GRIEVANCES UPDATE REQUESTED DATA CHANGE AS OWNER'), ('GRIEVANCES_ADD_NOTE', 'GRIEVANCES ADD NOTE'), ('GRIEVANCES_ADD_NOTE_AS_CREATOR', 'GRIEVANCES ADD NOTE AS CREATOR'), ('GRIEVANCES_ADD_NOTE_AS_OWNER', 'GRIEVANCES ADD NOTE AS OWNER'), ('GRIEVANCES_SET_IN_PROGRESS', 'GRIEVANCES SET IN PROGRESS'), ('GRIEVANCES_SET_IN_PROGRESS_AS_CREATOR', 'GRIEVANCES SET IN PROGRESS AS CREATOR'), ('GRIEVANCES_SET_IN_PROGRESS_AS_OWNER', 'GRIEVANCES SET IN PROGRESS AS OWNER'), ('GRIEVANCES_SET_ON_HOLD', 'GRIEVANCES SET ON HOLD'), ('GRIEVANCES_SET_ON_HOLD_AS_CREATOR', 'GRIEVANCES SET ON HOLD AS CREATOR'), ('GRIEVANCES_SET_ON_HOLD_AS_OWNER', 'GRIEVANCES SET ON HOLD AS OWNER'), ('GRIEVANCES_SEND_FOR_APPROVAL', 'GRIEVANCES SEND FOR APPROVAL'), ('GRIEVANCES_SEND_FOR_APPROVAL_AS_CREATOR', 'GRIEVANCES SEND FOR APPROVAL AS CREATOR'), ('GRIEVANCES_SEND_FOR_APPROVAL_AS_OWNER', 'GRIEVANCES SEND FOR APPROVAL AS OWNER'), ('GRIEVANCES_SEND_BACK', 'GRIEVANCES SEND BACK'), ('GRIEVANCES_SEND_BACK_AS_CREATOR', 'GRIEVANCES SEND BACK AS CREATOR'), ('GRIEVANCES_SEND_BACK_AS_OWNER', 'GRIEVANCES SEND BACK AS OWNER'), ('GRIEVANCES_APPROVE_DATA_CHANGE', 'GRIEVANCES APPROVE DATA CHANGE'), ('GRIEVANCES_APPROVE_DATA_CHANGE_AS_CREATOR', 'GRIEVANCES APPROVE DATA CHANGE AS CREATOR'), ('GRIEVANCES_APPROVE_DATA_CHANGE_AS_OWNER', 'GRIEVANCES APPROVE DATA CHANGE AS OWNER'), ('GRIEVANCES_UNDO_APPROVED_DATA_CHANGE', 'GRIEVANCES UNDO APPROVED DATA CHANGE'), ('GRIEVANCES_UNDO_APPROVED_DATA_CHANGE_AS_CREATOR', 'GRIEVANCES UNDO APPROVED DATA CHANGE AS CREATOR'), ('GRIEVANCES_UNDO_APPROVED_DATA_CHANGE_AS_OWNER', 'GRIEVANCES UNDO APPROVED DATA CHANGE AS OWNER'), ('GRIEVANCES_APPROVE_FLAG_AND_DEDUPE', 'GRIEVANCES APPROVE FLAG AND DEDUPE'), ('GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_CREATOR', 'GRIEVANCES APPROVE FLAG AND DEDUPE AS CREATOR'), ('GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_OWNER', 'GRIEVANCES APPROVE FLAG AND DEDUPE AS OWNER'), ('GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK', 'GRIEVANCES CLOSE TICKET EXCLUDING FEEDBACK'), ('GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_CREATOR', 'GRIEVANCES CLOSE TICKET EXCLUDING FEEDBACK AS CREATOR'), ('GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_OWNER', 'GRIEVANCES CLOSE TICKET EXCLUDING FEEDBACK AS OWNER'), ('GRIEVANCES_CLOSE_TICKET_FEEDBACK', 'GRIEVANCES CLOSE TICKET FEEDBACK'), ('GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_CREATOR', 'GRIEVANCES CLOSE TICKET FEEDBACK AS CREATOR'), ('GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_OWNER', 'GRIEVANCES CLOSE TICKET FEEDBACK AS OWNER')], max_length=255), blank=True, null=True, size=None),
        ),
    ]
