from typing import Any, List
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser

from parameterized import parameterized

from hct_mis_api.apps.account.fixtures import PartnerFactory, UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import (
    create_afghanistan,
    generate_data_collecting_types,
)
from hct_mis_api.apps.core.models import BusinessArea, DataCollectingType
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program, ProgramPartnerThrough


class TestAllProgramsQuery(APITestCase):
    ALL_PROGRAMS_QUERY = """
    query AllPrograms($businessArea: String!, $orderBy: String, $compatibleDct: Boolean) {
        allPrograms(businessArea: $businessArea, orderBy: $orderBy, compatibleDct: $compatibleDct) {
          totalCount
          edges {
            node {
              name
            }
          }
        }
      }
    """

    @classmethod
    def setUpTestData(cls) -> None:
        create_afghanistan()
        generate_data_collecting_types()
        data_collecting_type = DataCollectingType.objects.get(code="full_collection")
        cls.data_collecting_type_compatible = DataCollectingType.objects.get(code="size_only")
        cls.data_collecting_type_compatible.compatible_types.add(cls.data_collecting_type_compatible)
        data_collecting_type.compatible_types.add(cls.data_collecting_type_compatible, data_collecting_type)

        cls.business_area = BusinessArea.objects.get(slug="afghanistan")
        cls.business_area.data_collecting_types.set(DataCollectingType.objects.all().values_list("id", flat=True))

        cls.partner = PartnerFactory(name="WFP")
        cls.partner.allowed_business_areas.add(cls.business_area)
        cls.user = UserFactory.create(partner=cls.partner)

        cls.unicef_partner = PartnerFactory(name="UNICEF")
        other_partner = PartnerFactory(name="Other Partner")
        other_partner.allowed_business_areas.add(cls.business_area)

        program_with_partner_access = ProgramFactory.create(
            name="Program with partner access",
            status=Program.DRAFT,
            business_area=cls.business_area,
            data_collecting_type=data_collecting_type,
            partner_access=Program.SELECTED_PARTNERS_ACCESS,
        )
        ProgramPartnerThrough.objects.create(
            program=program_with_partner_access,
            partner=cls.partner,
        )

        ProgramFactory.create(
            name="Program with all partners access",
            status=Program.ACTIVE,
            business_area=cls.business_area,
            data_collecting_type=data_collecting_type,
            partner_access=Program.ALL_PARTNERS_ACCESS,
        )

        ProgramFactory.create(
            name="Program with none partner access",
            status=Program.ACTIVE,
            business_area=cls.business_area,
            data_collecting_type=data_collecting_type,
            partner_access=Program.NONE_PARTNERS_ACCESS,
        )

        program_without_partner_access = ProgramFactory.create(
            name="Program without partner access",
            status=Program.ACTIVE,
            business_area=cls.business_area,
            data_collecting_type=data_collecting_type,
            partner_access=Program.SELECTED_PARTNERS_ACCESS,
        )
        ProgramPartnerThrough.objects.create(
            program=program_without_partner_access,
            partner=other_partner,
        )

    @parameterized.expand(
        [
            ("with_permission", [Permissions.PROGRAMME_VIEW_LIST_AND_DETAILS]),
            ("without_permission", []),
        ]
    )
    def test_all_programs_query(self, _: Any, permissions: List[Permissions]) -> None:
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)
        self.snapshot_graphql_request(
            request_string=self.ALL_PROGRAMS_QUERY,
            context={
                "user": self.user,
                "headers": {
                    "Business-Area": self.business_area.slug,
                },
            },
            variables={"businessArea": self.business_area.slug, "orderBy": "name"},
        )

    def test_all_programs_query_unicef_partner(self) -> None:
        user = UserFactory.create(partner=self.unicef_partner)
        # granting any role in the business area to the user; permission to view programs is inherited from the unicef partner
        self.create_user_role_with_permissions(user, [Permissions.RDI_MERGE_IMPORT], self.business_area)
        self.snapshot_graphql_request(
            request_string=self.ALL_PROGRAMS_QUERY,
            context={
                "user": user,
                "headers": {
                    "Business-Area": self.business_area.slug,
                },
            },
            variables={"businessArea": self.business_area.slug, "orderBy": "name"},
        )

    def test_all_programs_query_filter_dct(self) -> None:
        program = ProgramFactory.create(
            name="Program for dct filter",
            status=Program.ACTIVE,
            business_area=self.business_area,
            data_collecting_type=self.data_collecting_type_compatible,
            partner_access=Program.ALL_PARTNERS_ACCESS,
        )
        # program that does not have the current program in the compatible types
        ProgramFactory.create(
            name="Program not compatible",
            status=Program.ACTIVE,
            business_area=self.business_area,
            data_collecting_type=DataCollectingType.objects.get(code="partial_individuals"),
            partner_access=Program.ALL_PARTNERS_ACCESS,
        )

        user = UserFactory.create(partner=self.unicef_partner)
        self.create_user_role_with_permissions(user, [Permissions.RDI_MERGE_IMPORT], self.business_area)
        self.snapshot_graphql_request(
            request_string=self.ALL_PROGRAMS_QUERY,
            context={
                "user": user,
                "headers": {
                    "Business-Area": self.business_area.slug,
                    "Program": self.id_to_base64(program.id, "ProgramNode"),
                },
            },
            variables={"businessArea": self.business_area.slug, "orderBy": "name", "compatibleDct": True},
        )

    @patch("django.contrib.auth.models.AnonymousUser.is_authenticated", new_callable=lambda: False)
    def test_all_programs_query_user_not_authenticated(self, mock_is_authenticated: Any) -> None:
        self.snapshot_graphql_request(
            request_string=self.ALL_PROGRAMS_QUERY,
            context={
                "user": AnonymousUser,
                "headers": {
                    "Business-Area": self.business_area.slug,
                },
            },
            variables={"businessArea": self.business_area.slug, "orderBy": "name"},
        )
