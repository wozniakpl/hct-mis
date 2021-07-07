import graphene

from hct_mis_api.apps.core.utils import decode_and_get_object
from hct_mis_api.apps.grievance.models import (
    TicketNegativeFeedbackDetails,
    TicketPositiveFeedbackDetails,
)
from hct_mis_api.apps.household.models import Household, Individual
from hct_mis_api.apps.household.schema import HouseholdNode, IndividualNode


class PositiveFeedbackTicketExtras(graphene.InputObjectType):
    household = graphene.GlobalID(node=HouseholdNode, required=False)
    individual = graphene.GlobalID(node=IndividualNode, required=False)


class NegativeFeedbackTicketExtras(graphene.InputObjectType):
    household = graphene.GlobalID(node=HouseholdNode, required=False)
    individual = graphene.GlobalID(node=IndividualNode, required=False)


def save_positive_feedback_extras(root, info, input, grievance_ticket, extras, **kwargs):
    category_extras = extras.get("category", {})
    feedback_ticket_extras = category_extras.get("positive_feedback_ticket_extras", {})

    individual_encoded_id = feedback_ticket_extras.get("individual")
    individual = decode_and_get_object(individual_encoded_id, Individual, False)

    household_encoded_id = feedback_ticket_extras.get("household")
    household = decode_and_get_object(household_encoded_id, Household, False)

    TicketPositiveFeedbackDetails.objects.create(
        individual=individual,
        household=household,
        ticket=grievance_ticket,
    )
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]


def save_negative_feedback_extras(root, info, input, grievance_ticket, extras, **kwargs):
    category_extras = extras.get("category", {})
    feedback_ticket_extras = category_extras.get("negative_feedback_ticket_extras", {})

    individual_encoded_id = feedback_ticket_extras.get("individual")
    individual = decode_and_get_object(individual_encoded_id, Individual, False)

    household_encoded_id = feedback_ticket_extras.get("household")
    household = decode_and_get_object(household_encoded_id, Household, False)

    TicketNegativeFeedbackDetails.objects.create(
        individual=individual,
        household=household,
        ticket=grievance_ticket,
    )
    grievance_ticket.refresh_from_db()
    return [grievance_ticket]
