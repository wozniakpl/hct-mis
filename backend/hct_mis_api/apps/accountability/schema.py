from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from hct_mis_api.apps.account.permissions import (
    BaseNodePermissionMixin,
    DjangoPermissionFilterConnectionField,
    Permissions,
    hopeOneOfPermissionClass,
)
from hct_mis_api.apps.core.extended_connection import ExtendedConnection
from hct_mis_api.apps.core.schema import ChoiceObject
from hct_mis_api.apps.core.utils import decode_id_string, to_choice_object
from hct_mis_api.apps.household.models import Household

from ..program.models import Program
from ..program.schema import ProgramNode
from ..targeting.graphql_types import TargetPopulationNode
from ..targeting.models import TargetPopulation
from .filters import (
    FeedbackFilter,
    MessageRecipientsMapFilter,
    MessagesFilter,
    RecipientFilter,
    SurveyFilter,
)
from .inputs import (
    AccountabilitySampleSizeInput,
    GetAccountabilityCommunicationMessageSampleSizeInput,
)
from .models import Feedback, FeedbackMessage, Message, Survey
from .services.message_crud_services import MessageCrudServices
from .services.sampling import Sampling
from .services.verifiers import MessageArgumentVerifier


class CommunicationMessageRecipientMapNode(DjangoObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_LIST,
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_DETAILS,
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_DETAILS_AS_CREATOR,
        ),
    )

    class Meta:
        model = Household
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection
        filter_fields = []
        fields = (
            "id",
            "size",
            "head_of_household",
        )


class CommunicationMessageNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_LIST,
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_DETAILS,
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_DETAILS_AS_CREATOR,
        ),
    )

    class Meta:
        model = Message
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection
        filter_fields = []


class FeedbackMessageNode(DjangoObjectType):
    class Meta:
        model = FeedbackMessage
        exclude = ("feedback",)
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection


class FeedbackNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_FEEDBACK_VIEW_LIST,
            Permissions.ACCOUNTABILITY_FEEDBACK_VIEW_DETAILS,
        ),
    )

    class Meta:
        model = Feedback
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection
        filter_fields = []


class GetCommunicationMessageSampleSizeObject(BaseNodePermissionMixin, graphene.ObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_COMMUNICATION_MESSAGE_VIEW_DETAILS,
        ),
    )

    number_of_recipients = graphene.Int()
    sample_size = graphene.Int()


class SurveyNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_SURVEY_VIEW_LIST,
            Permissions.ACCOUNTABILITY_SURVEY_VIEW_DETAILS,
        ),
    )

    class Meta:
        model = Survey
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection
        filter_fields = []


class RecipientNode(BaseNodePermissionMixin, DjangoObjectType):
    permission_classes = (
        hopeOneOfPermissionClass(
            Permissions.ACCOUNTABILITY_SURVEY_VIEW_DETAILS,
        ),
    )

    class Meta:
        model = Household
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection
        filter_fields = []
        fields = (
            "id",
            "size",
            "head_of_household",
        )


class AccountabilitySampleSizeObject(graphene.ObjectType):
    number_of_recipients = graphene.Int()
    sample_size = graphene.Int()


class Query(graphene.ObjectType):
    accountability_communication_message = graphene.relay.Node.Field(CommunicationMessageNode)
    all_accountability_communication_messages = DjangoPermissionFilterConnectionField(
        CommunicationMessageNode,
        filterset_class=MessagesFilter,
    )

    accountability_communication_message_recipient = graphene.relay.Node.Field(CommunicationMessageRecipientMapNode)
    all_accountability_communication_message_recipients = DjangoPermissionFilterConnectionField(
        CommunicationMessageRecipientMapNode,
        filterset_class=MessageRecipientsMapFilter,
    )

    accountability_communication_message_sample_size = graphene.Field(
        GetCommunicationMessageSampleSizeObject,
        business_area_slug=graphene.String(required=True),
        inputs=GetAccountabilityCommunicationMessageSampleSizeInput(),
    )

    feedback = graphene.relay.Node.Field(FeedbackNode)
    all_feedbacks = DjangoPermissionFilterConnectionField(
        FeedbackNode,
        filterset_class=FeedbackFilter,
    )

    feedback_issue_type_choices = graphene.List(ChoiceObject)

    survey = graphene.relay.Node.Field(SurveyNode)
    all_surveys = DjangoPermissionFilterConnectionField(
        SurveyNode,
        filterset_class=SurveyFilter,
        permission_classes=(hopeOneOfPermissionClass(Permissions.ACCOUNTABILITY_SURVEY_VIEW_LIST),),
    )
    recipients = DjangoPermissionFilterConnectionField(
        RecipientNode,
        filterset_class=RecipientFilter,
        permission_classes=(hopeOneOfPermissionClass(Permissions.ACCOUNTABILITY_SURVEY_VIEW_DETAILS),),
    )
    accountability_sample_size = graphene.Field(
        AccountabilitySampleSizeObject,
        input=AccountabilitySampleSizeInput(),
    )
    all_target_population_for_accountability = DjangoFilterConnectionField(
        TargetPopulationNode,
        permission_classes=(hopeOneOfPermissionClass(Permissions.ACCOUNTABILITY_SURVEY_VIEW_LIST),),
    )
    all_program_for_accountability = DjangoFilterConnectionField(
        ProgramNode,
        permission_classes=(hopeOneOfPermissionClass(Permissions.ACCOUNTABILITY_SURVEY_VIEW_LIST),),
    )

    def resolve_feedback_issue_type_choices(self, info, **kwargs):
        return to_choice_object(Feedback.ISSUE_TYPE_CHOICES)

    def resolve_accountability_communication_message_sample_size(
        self, info, business_area_slug: str, inputs: dict, **kwargs
    ):
        verifier = MessageArgumentVerifier(inputs)
        verifier.verify()

        households = MessageCrudServices._get_households(inputs)

        sampling = Sampling(inputs, households)
        number_of_recipients, sample_size = sampling.generate_sampling()

        return {
            "number_of_recipients": number_of_recipients,
            "sample_size": sample_size,
        }

    def resolve_accountability_sample_size(self, info, input: dict, **kwargs):
        if target_population := input.get("target_population"):
            obj = get_object_or_404(TargetPopulation, id=decode_id_string(target_population))
            households = Household.objects.filter(target_populations=obj)
        elif program := input.get("program"):
            obj = get_object_or_404(Program, id=decode_id_string(program))
            households = Household.objects.filter(target_populations__program=obj)
        else:
            raise ValidationError("Target population or program should be provided.")

        sampling = Sampling(input, households)
        number_of_recipients, sample_size = sampling.generate_sampling()

        return {
            "number_of_recipients": number_of_recipients,
            "sample_size": sample_size,
        }

    def resolve_target_population_for_accountability(self, info, **kwargs):
        return TargetPopulation.objects.exclude(status=TargetPopulation.STATUS_OPEN).filter(
            business_area__slug=info.context.headers.get("Business-Area").lower()
        )

    def resolve_program_for_accountability(self, info, **kwargs):
        return Program.objects.exclude(status=Program.DRAFT).filter(
            business_area__slug=info.context.headers.get("Business-Area").lower()
        )
