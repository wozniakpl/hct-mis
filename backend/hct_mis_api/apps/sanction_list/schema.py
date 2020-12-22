import graphene
from django.db.models.functions import Lower
from django_filters import FilterSet
from graphene import relay
from graphene_django import DjangoObjectType

from account.permissions import DjangoPermissionFilterConnectionField
from core.extended_connection import ExtendedConnection
from core.utils import CustomOrderingFilter
from sanction_list.models import (
    SanctionListIndividual,
    SanctionListIndividualDocument,
    SanctionListIndividualNationalities,
    SanctionListIndividualCountries,
    SanctionListIndividualAliasName,
    SanctionListIndividualDateOfBirth,
)


class SanctionListIndividualFilter(FilterSet):
    class Meta:
        fields = {
            "id": ["exact"],
            "full_name": ["exact", "icontains"],
            "reference_number": ["exact"],
        }
        model = SanctionListIndividual

    order_by = CustomOrderingFilter(
        fields=(
            "id",
            "reference_number",
            Lower("full_name"),
            "listed_on",
        )
    )


class SanctionListIndividualNode(DjangoObjectType):
    country_of_birth = graphene.String(description="Country of birth")

    class Meta:
        model = SanctionListIndividual
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_country_of_birth(parent, info):
        return parent.country_of_birth.name


class SanctionListIndividualDocumentNode(DjangoObjectType):
    issuing_country = graphene.String(description="Issuing country name")

    class Meta:
        model = SanctionListIndividualDocument
        exclude = ("individual",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_issuing_country(parent, info):
        return parent.issuing_country.name


class SanctionListIndividualNationalitiesNode(DjangoObjectType):
    nationality = graphene.String()

    class Meta:
        model = SanctionListIndividualNationalities
        exclude = ("individual",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_nationality(parent, info):
        return parent.nationality.name


class SanctionListIndividualCountriesNode(DjangoObjectType):
    country = graphene.String()

    class Meta:
        model = SanctionListIndividualCountries
        exclude = ("individual",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    def resolve_country(parent, info):
        return parent.country.name


class SanctionListIndividualAliasNameNode(DjangoObjectType):
    class Meta:
        model = SanctionListIndividualAliasName
        exclude = ("individual",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class SanctionListIndividualDateOfBirthNode(DjangoObjectType):
    class Meta:
        model = SanctionListIndividualDateOfBirth
        exclude = ("individual",)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class Query(graphene.ObjectType):
    sanction_list_individual = relay.Node.Field(SanctionListIndividualNode)
    all_sanction_list_individuals = DjangoPermissionFilterConnectionField(
        SanctionListIndividualNode,
        filterset_class=SanctionListIndividualFilter,
    )
