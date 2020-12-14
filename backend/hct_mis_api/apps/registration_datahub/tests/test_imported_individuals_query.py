from parameterized import parameterized
from django.core.management import call_command

from account.fixtures import UserFactory
from account.permissions import Permissions
from core.base_test_case import APITestCase
from registration_datahub.fixtures import ImportedIndividualFactory
from core.models import BusinessArea

ALL_IMPORTED_INDIVIDUALS_QUERY = """
query AllImportedIndividuals {
  allImportedIndividuals(businessArea: "afghanistan") {
    edges {
      node {
        fullName
        givenName
        familyName
        phoneNo
        birthDate
      }
    }
  }
}
"""
ALL_IMPORTED_INDIVIDUALS_ORDER_BY_BIRTH_DATE_A_QUERY = """
query AllImportedIndividuals {
  allImportedIndividuals(orderBy: "birth_date", businessArea: "afghanistan") {
    edges {
      node {
        fullName
        givenName
        familyName
        phoneNo
        birthDate
      }
    }
  }
}
"""
ALL_IMPORTED_INDIVIDUALS_ORDER_BY_BIRTH_DATE_D_QUERY = """
query AllImportedIndividuals {
  allImportedIndividuals(orderBy: "-birth_date", businessArea: "afghanistan") {
    edges {
      node {
        fullName
        givenName
        familyName
        phoneNo
        birthDate
      }
    }
  }
}
"""
IMPORTED_INDIVIDUAL_QUERY = """
query ImportedIndividual($id: ID!) {
  importedIndividual(id: $id) {
    fullName
    givenName
    familyName
    phoneNo
    birthDate
  }
}
"""


class TestImportedIndividualQuery(APITestCase):
    multi_db = True

    # IMPORTANT!
    # FREEZGUN doesn't work this snapshot have to be updated once a year
    MAX_AGE = 51
    MIN_AGE = 37

    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        call_command("loadbusinessareas")
        self.business_area = BusinessArea.objects.get(slug="afghanistan")
        self.individuals_to_create = [
            {
                "full_name": "Benjamin Butler",
                "given_name": "Benjamin",
                "family_name": "Butler",
                "phone_no": "(953)682-4596",
                "birth_date": "1943-07-30",
                "sex": "MALE",
            },
            {
                "full_name": "Robin Ford",
                "given_name": "Robin",
                "family_name": "Ford",
                "phone_no": "+18663567905",
                "birth_date": "1946-02-15",
                "sex": "MALE",
            },
            {
                "full_name": "Timothy Perry",
                "given_name": "Timothy",
                "family_name": "Perry",
                "phone_no": "(548)313-1700-902",
                "birth_date": "1983-12-21",
                "sex": "MALE",
            },
            {
                "full_name": "Eric Torres",
                "given_name": "Eric",
                "family_name": "Torres",
                "phone_no": "(228)231-5473",
                "birth_date": "1973-03-23",
                "sex": "MALE",
            },
            {
                "full_name": "Jenna Franklin",
                "given_name": "Jenna",
                "family_name": "Franklin",
                "phone_no": "001-296-358-5428-607",
                "birth_date": "1969-11-29",
                "sex": "FEMALE",
            },
        ]

        self.individuals = [ImportedIndividualFactory(**individual) for individual in self.individuals_to_create]
        for individual in self.individuals:
            individual.registration_data_import.business_area_slug = "afghanistan"
            individual.registration_data_import.save()

    @parameterized.expand(
        [
            ("all_with_permission", [Permissions.RDI_VIEW_DETAILS], ALL_IMPORTED_INDIVIDUALS_QUERY),
            ("all_without_permission", [], ALL_IMPORTED_INDIVIDUALS_QUERY),
            (
                "order_by_dob_all_with_permission",
                [Permissions.RDI_VIEW_DETAILS],
                ALL_IMPORTED_INDIVIDUALS_ORDER_BY_BIRTH_DATE_A_QUERY,
            ),
            (
                "order_by_dob_d_all_with_permission",
                [Permissions.RDI_VIEW_DETAILS],
                ALL_IMPORTED_INDIVIDUALS_ORDER_BY_BIRTH_DATE_D_QUERY,
            ),
        ]
    )
    def test_imported_individual_query(self, _, permissions, query):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=query,
            context={"user": self.user},
        )

    @parameterized.expand(
        [
            ("with_permission", [Permissions.RDI_VIEW_DETAILS]),
            ("without_permission", []),
        ]
    )
    def test_imported_individual_query_single(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=IMPORTED_INDIVIDUAL_QUERY,
            context={"user": self.user},
            variables={
                "id": self.id_to_base64(
                    self.individuals[0].id,
                    "ImportedIndividualNode",
                )
            },
        )
