from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import (
    AdminAreaFactory,
    AdminAreaLevelFactory,
    create_afghanistan,
)
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.geo.fixtures import AreaFactory, AreaTypeFactory
from hct_mis_api.apps.geo.models import Country
from hct_mis_api.apps.grievance.models import GrievanceTicket, TicketNeedsAdjudicationDetails
from hct_mis_api.apps.household.fixtures import create_household
from hct_mis_api.apps.household.models import Household


class TestGrievanceQuerySearchFilter(APITestCase):
    FILTER_BY_SEARCH = """
    query AllGrievanceTicket($search: String) 
    {
      allGrievanceTicket(businessArea: "afghanistan", search: $search) {
        totalCount
        edges {
          cursor
          node {
            description
          }
        }
      }
    }
    """

    @classmethod
    def setUpTestData(cls):
        create_afghanistan()
        cls.user = UserFactory.create()
        cls.user2 = UserFactory.create()
        cls.business_area = BusinessArea.objects.get(slug="afghanistan")
        area_type = AdminAreaLevelFactory(
            name="Admin type one",
            admin_level=2,
            business_area=cls.business_area,
        )
        cls.admin_area_1 = AdminAreaFactory(title="City Test", admin_area_level=area_type, p_code="123aa123")
        cls.admin_area_2 = AdminAreaFactory(title="City Example", admin_area_level=area_type, p_code="sadasdasfd222")

        country = Country.objects.first()
        area_type_new = AreaTypeFactory(
            name="Admin type one",
            area_level=2,
            country=country,
            original_id=area_type.id,
        )
        cls.admin_area_1_new = AreaFactory(
            name="City Test", area_type=area_type_new, p_code="123aa123", original_id=cls.admin_area_1.id
        )
        cls.admin_area_2_new = AreaFactory(
            name="City Example", area_type=area_type_new, p_code="sadasdasfd222", original_id=cls.admin_area_2.id
        )

        _, individuals = create_household({"size": 2}, {"family_name": "Kowalski"})
        cls.individual_1 = individuals[0]
        cls.individual_2 = individuals[1]

        Household.objects.all().update(unicef_id="HH-22-0059.7225")

        grievance_ticket_1 = GrievanceTicket(
            **{
                "business_area": cls.business_area,
                "admin2": cls.admin_area_1,
                "admin2_new": cls.admin_area_1_new,
                "language": "Polish",
                "consent": True,
                "description": "ticket_1",
                "category": GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
                "status": GrievanceTicket.STATUS_NEW,
                "created_by": cls.user,
                "assigned_to": cls.user,
                "household_unicef_id": "HH-22-0059.7223"
            }
        )

        grievance_ticket_2 = GrievanceTicket(
            **{
                "business_area": cls.business_area,
                "admin2": cls.admin_area_2,
                "admin2_new": cls.admin_area_2_new,
                "language": "English",
                "consent": True,
                "description": "ticket_2",
                "category": GrievanceTicket.CATEGORY_NEGATIVE_FEEDBACK,
                "status": GrievanceTicket.STATUS_ON_HOLD,
                "created_by": cls.user,
                "assigned_to": cls.user,
                "household_unicef_id": "HH-22-0059.7224"
            }
        )

        grievance_ticket_3 = GrievanceTicket(
            **{
                "business_area": cls.business_area,
                "admin2": cls.admin_area_2,
                "admin2_new": cls.admin_area_2_new,
                "language": "Polish, English",
                "consent": True,
                "description": "ticket_3",
                "category": GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
                "status": GrievanceTicket.STATUS_IN_PROGRESS,
                "created_by": cls.user,
                "assigned_to": cls.user,
                "household_unicef_id": "HH-22-0059.7225"
            }
        )

        GrievanceTicket.objects.bulk_create((
            grievance_ticket_1,
            grievance_ticket_2,
            grievance_ticket_3
        ))

        cls.grievance_ticket_1 = GrievanceTicket.objects.get(household_unicef_id="HH-22-0059.7223")
        cls.grievance_ticket_2 = GrievanceTicket.objects.get(household_unicef_id="HH-22-0059.7224")
        cls.grievance_ticket_3 = GrievanceTicket.objects.get(household_unicef_id="HH-22-0059.7225")

    def test_grievance_list_filtered_by_ticket_id(self):
        self.create_user_role_with_permissions(
            self.user,
            [Permissions.GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE, Permissions.GRIEVANCES_VIEW_LIST_SENSITIVE],
            self.business_area,
        )

        self.snapshot_graphql_request(
            request_string=self.FILTER_BY_SEARCH,
            context={"user": self.user},
            variables={"search": f"ticket_id {self.grievance_ticket_1.unicef_id}"},
        )

    def test_grievance_list_filtered_by_ticket_household_unicef_id(self):
        self.create_user_role_with_permissions(
            self.user,
            [Permissions.GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE, Permissions.GRIEVANCES_VIEW_LIST_SENSITIVE],
            self.business_area,
        )

        self.snapshot_graphql_request(
            request_string=self.FILTER_BY_SEARCH,
            context={"user": self.user},
            variables={"search": f"ticket_hh_id {self.grievance_ticket_2.household_unicef_id}"},
        )

    def test_grievance_list_filtered_by_household_head_family_name(self):
        self.create_user_role_with_permissions(
            self.user,
            [Permissions.GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE, Permissions.GRIEVANCES_VIEW_LIST_SENSITIVE],
            self.business_area,
        )

        self.snapshot_graphql_request(
            request_string=self.FILTER_BY_SEARCH,
            context={"user": self.user},
            variables={"search": f"family_name {self.individual_1.family_name}"},
        )
