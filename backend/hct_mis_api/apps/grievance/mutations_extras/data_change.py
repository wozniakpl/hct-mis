import graphene
from django.shortcuts import get_object_or_404
from graphene.utils.str_converters import to_snake_case

from core.utils import decode_id_string
from grievance.models import (
    GrievanceTicket,
    TicketIndividualDataUpdateDetails,
    TicketAddIndividualDetails,
    TicketDeleteIndividualDetails,
    TicketHouseholdDataUpdateDetails,
)
from household.models import Individual, Household
from household.schema import HouseholdNode, IndividualNode


class HouseholdUpdateDataObjectType(graphene.InputObjectType):
    status = graphene.String()
    consent = graphene.Boolean()
    residence_status = graphene.String()
    country_origin = graphene.String()
    country = graphene.String()
    size = graphene.Int()
    address = graphene.String()
    female_age_group_0_5_count = graphene.Int()
    female_age_group_6_11_count = graphene.Int()
    female_age_group_12_17_count = graphene.Int()
    female_adults_count = graphene.Int()
    pregnant_count = graphene.Int()
    male_age_group_0_5_count = graphene.Int()
    male_age_group_6_11_count = graphene.Int()
    male_age_group_12_17_count = graphene.Int()
    male_adults_count = graphene.Int()
    female_age_group_0_5_disabled_count = graphene.Int()
    female_age_group_6_11_disabled_count = graphene.Int()
    female_age_group_12_17_disabled_count = graphene.Int()
    female_adults_disabled_count = graphene.Int()
    male_age_group_0_5_disabled_count = graphene.Int()
    male_age_group_6_11_disabled_count = graphene.Int()
    male_age_group_12_17_disabled_count = graphene.Int()
    male_adults_disabled_count = graphene.Int()
    returnee = graphene.Boolean()
    fchild_hoh = graphene.Boolean()
    child_hoh = graphene.Boolean()
    start = graphene.DateTime()
    end = graphene.DateTime()
    name_enumerator = graphene.String()
    org_enumerator = graphene.String()
    org_name_enumerator = graphene.String()
    village = graphene.String()


class IndividualUpdateDataObjectType(graphene.InputObjectType):
    status = graphene.String()
    full_name = graphene.String()
    given_name = graphene.String()
    middle_name = graphene.String()
    family_name = graphene.String()
    sex = graphene.String()
    birth_date = graphene.Date()
    estimated_birth_date = graphene.Boolean()
    marital_status = graphene.String()
    phone_no = graphene.String()
    phone_no_alternative = graphene.String()
    relationship = graphene.String()
    disability = graphene.Boolean()
    work_status = graphene.String()
    enrolled_in_nutrition_programme = graphene.Boolean()
    administration_of_rutf = graphene.Boolean()
    pregnant = graphene.Boolean()
    observed_disability = graphene.List(graphene.String)
    seeing_disability = graphene.String()
    hearing_disability = graphene.String()
    physical_disability = graphene.String()
    memory_disability = graphene.String()
    selfcare_disability = graphene.String()
    comms_disability = graphene.String()
    who_answers_phone = graphene.String()
    who_answers_alt_phone = graphene.String()


class AddIndividualDataObjectType(graphene.InputObjectType):
    full_name = graphene.String(required=True)
    given_name = graphene.String(required=True)
    middle_name = graphene.String()
    family_name = graphene.String(required=True)
    sex = graphene.String(required=True)
    birth_date = graphene.Date()
    estimated_birth_date = graphene.Boolean()
    marital_status = graphene.String()
    phone_no = graphene.String()
    phone_no_alternative = graphene.String()
    relationship = graphene.String()
    disability = graphene.Boolean()
    work_status = graphene.String()
    enrolled_in_nutrition_programme = graphene.Boolean()
    administration_of_rutf = graphene.Boolean()
    pregnant = graphene.Boolean()
    observed_disability = graphene.List(graphene.String)
    seeing_disability = graphene.String()
    hearing_disability = graphene.String()
    physical_disability = graphene.String()
    memory_disability = graphene.String()
    selfcare_disability = graphene.String()
    comms_disability = graphene.String()
    who_answers_phone = graphene.String()
    who_answers_alt_phone = graphene.String()


class HouseholdDataUpdateIssueTypeExtras(graphene.InputObjectType):
    household = graphene.GlobalID(node=HouseholdNode, required=True)
    household_data = HouseholdUpdateDataObjectType()


class IndividualDataUpdateIssueTypeExtras(graphene.InputObjectType):
    individual = graphene.GlobalID(node=IndividualNode, required=True)
    individual_data = IndividualUpdateDataObjectType(required=True)


class AddIndividualIssueTypeExtras(graphene.InputObjectType):
    household = graphene.GlobalID(node=HouseholdNode, required=True)
    individual_data = AddIndividualDataObjectType(required=True)


class IndividualDeleteIssueTypeExtras(graphene.InputObjectType):
    individual = graphene.GlobalID(node=IndividualNode, required=True)


def save_data_change_extras(root, info, input, grievance_ticket, extras, **kwargs):
    issue_type = input.get("issue_type")
    if issue_type == GrievanceTicket.ISSUE_TYPE_INDIVIDUAL_DATA_CHANGE_DATA_UPDATE:
        return save_individual_data_update_extras(root, info, input, grievance_ticket, extras, **kwargs)
    if issue_type == GrievanceTicket.ISSUE_TYPE_DATA_CHANGE_ADD_INDIVIDUAL:
        return save_add_individual_extras(root, info, input, grievance_ticket, extras, **kwargs)
    if issue_type == GrievanceTicket.ISSUE_TYPE_DATA_CHANGE_DELETE_INDIVIDUAL:
        return save_individual_delete_extras(root, info, input, grievance_ticket, extras, **kwargs)
    if issue_type == GrievanceTicket.ISSUE_TYPE_HOUSEHOLD_DATA_CHANGE_DATA_UPDATE:
        return save_household_data_update_extras(root, info, input, grievance_ticket, extras, **kwargs)


def save_household_data_update_extras(root, info, input, grievance_ticket, extras, **kwargs):
    data_change_extras = extras.get("issue_type")
    household_data_update_issue_type_extras = data_change_extras.get("household_data_update_issue_type_extras")

    household_encoded_id = household_data_update_issue_type_extras.get("household")
    household_id = decode_id_string(household_encoded_id)
    household = get_object_or_404(Household, id=household_id)
    household_data = {
        to_snake_case(key): value
        for key, value in household_data_update_issue_type_extras.get("household_data", {}).items()
    }
    ticket_individual_data_update_details = TicketHouseholdDataUpdateDetails(
        household_data=household_data, household=household, ticket=grievance_ticket,
    )
    ticket_individual_data_update_details.save()
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]


def save_individual_data_update_extras(root, info, input, grievance_ticket, extras, **kwargs):
    data_change_extras = extras.get("issue_type")
    individual_data_update_issue_type_extras = data_change_extras.get("individual_data_update_issue_type_extras")

    individual_encoded_id = individual_data_update_issue_type_extras.get("individual")
    individual_id = decode_id_string(individual_encoded_id)
    individual = get_object_or_404(Individual, id=individual_id)
    individual_data = individual_data_update_issue_type_extras.get("individual_data")
    birth_date = individual_data.get("birth_date")
    if birth_date:
        individual_data["birth_date"] = birth_date.isoformat()
    individual_data = {
        to_snake_case(key): value
        for key, value in individual_data_update_issue_type_extras.get("individual_data", {}).items()
    }
    ticket_individual_data_update_details = TicketIndividualDataUpdateDetails(
        individual_data=individual_data, individual=individual, ticket=grievance_ticket,
    )
    ticket_individual_data_update_details.save()
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]


def save_individual_delete_extras(root, info, input, grievance_ticket, extras, **kwargs):
    data_change_extras = extras.get("issue_type")
    individual_data_update_issue_type_extras = data_change_extras.get("individual_delete_issue_type_extras")

    individual_encoded_id = individual_data_update_issue_type_extras.get("individual")
    individual_id = decode_id_string(individual_encoded_id)
    individual = get_object_or_404(Individual, id=individual_id)
    ticket_individual_data_update_details = TicketDeleteIndividualDetails(
        individual=individual, ticket=grievance_ticket,
    )
    ticket_individual_data_update_details.save()
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]


def save_add_individual_extras(root, info, input, grievance_ticket, extras, **kwargs):
    data_change_extras = extras.get("issue_type")
    add_individual_issue_type_extras = data_change_extras.get("add_individual_issue_type_extras")

    household_encoded_id = add_individual_issue_type_extras.get("household")
    household_id = decode_id_string(household_encoded_id)
    household = get_object_or_404(Household, id=household_id)
    individual_data = add_individual_issue_type_extras.get("individual_data")
    birth_date = individual_data.get("birth_date")
    if birth_date:
        individual_data["birth_date"] = birth_date.isoformat()
    individual_data_with_approve_status = {
        to_snake_case(field): {"value": value, "approve_status": False} for field, value in individual_data
    }
    ticket_add_individual_details = TicketAddIndividualDetails(
        individual_data=individual_data_with_approve_status, household=household, ticket=grievance_ticket,
    )
    ticket_add_individual_details.save()
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]
