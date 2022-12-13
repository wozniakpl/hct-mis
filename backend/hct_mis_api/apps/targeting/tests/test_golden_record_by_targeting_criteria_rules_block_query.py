from django.core.management import call_command

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.fixtures import (
    BankAccountInfoFactory,
    create_household_and_individuals,
    create_individual_document,
)
from hct_mis_api.apps.household.models import MALE
from hct_mis_api.apps.household.services.household_recalculate_data import (
    recalculate_data,
)
from hct_mis_api.apps.program.fixtures import ProgramFactory


class GoldenRecordTargetingCriteriaWithBlockFiltersQueryTestCase(APITestCase):
    QUERY = """
        query GoldenRecordFilter(
            $targetingCriteria: TargetingCriteriaObjectType!,
            $program: ID!,
            $businessArea: String
          ) {
          goldenRecordByTargetingCriteria(
              targetingCriteria: $targetingCriteria,
              program: $program,
              businessArea: $businessArea,
              excludedIds: "",
              orderBy: "size"
            ) {
            totalCount
            edges {
              node {
                size
                individuals(orderBy: "sex", businessArea: $businessArea) {
                    edges{
                        node{
                            sex
                            maritalStatus
                        }
                    }
                }
              }
            }
          }
        }
        """

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("loadflexfieldsattributes")
        create_afghanistan()
        cls.business_area = BusinessArea.objects.first()
        cls.program = ProgramFactory(business_area=cls.business_area, individual_data_needed=True)
        (household, individuals) = create_household_and_individuals(
            {
                "business_area": cls.business_area,
            },
            [
                {
                    "sex": "MALE",
                    "marital_status": "MARRIED",
                    "observed_disability": ["SEEING", "HEARING", "WALKING", "MEMORY", "SELF_CARE", "COMMUNICATING"],
                    "seeing_disability": "LOT_DIFFICULTY",
                    "hearing_disability": "SOME_DIFFICULTY",
                    "physical_disability": "SOME_DIFFICULTY",
                    "memory_disability": "LOT_DIFFICULTY",
                    "selfcare_disability": "CANNOT_DO",
                    "comms_disability": "SOME_DIFFICULTY",
                    "business_area": cls.business_area,
                },
            ],
        )
        cls.household_targeted = household
        cls.targeted_inds = individuals
        (household, individuals) = create_household_and_individuals(
            {
                "business_area": cls.business_area,
            },
            [
                {
                    "sex": "MALE",
                    "marital_status": "SINGLE",
                    "business_area": cls.business_area,
                },
                {
                    "sex": "FEMALE",
                    "marital_status": "MARRIED",
                    "business_area": cls.business_area,
                },
            ],
        )
        cls.not_targeted_household = household
        cls.not_targeted_inds = individuals

        recalculate_data(cls.household_targeted)
        recalculate_data(cls.not_targeted_household)

        cls.user = UserFactory()
        cls.create_user_role_with_permissions(cls.user, [Permissions.TARGETING_CREATE], cls.business_area)

    def test_golden_record_by_targeting_criteria_size(self) -> None:
        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": ["MARRIED"],
                                        "fieldName": "marital_status",
                                        "isFlexField": False,
                                    },
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": [MALE],
                                        "fieldName": "sex",
                                        "isFlexField": False,
                                    },
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersQueryTestCase.QUERY,
            variables=variables,
        )

    def test_golden_record_by_targeting_criteria_observed_disability(self) -> None:
        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "CONTAINS",
                                        "arguments": [
                                            "COMMUNICATING",
                                            "HEARING",
                                            "MEMORY",
                                            "SEEING",
                                            "WALKING",
                                            "SELF_CARE",
                                        ],
                                        "fieldName": "observed_disability",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersQueryTestCase.QUERY,
            variables=variables,
        )

    # ruleFilters for observed_disability and fullname will be served with ts_vector
    def test_golden_record_by_targeting_criteria_observed_disability_with_valid_argument(self) -> None:
        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "CONTAINS",
                                        "arguments": [
                                            "COMMUNICATING",
                                            "HEARING",
                                            "MEMORY",
                                            "SEEING",
                                            "WALKING",
                                            "SELF_CARE",
                                        ],
                                        "fieldName": "observed_disability",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersQueryTestCase.QUERY,
            variables=variables,
        )


class GoldenRecordTargetingCriteriaWithBlockFiltersOtherQueryTestCase(APITestCase):
    """This class tests phone, bank_account_info and tax_id filters"""

    QUERY = """
        query GoldenRecordFilter($targetingCriteria: TargetingCriteriaObjectType!, $program: ID!, $businessArea: String) {
          goldenRecordByTargetingCriteria(targetingCriteria: $targetingCriteria, program: $program, businessArea: $businessArea, excludedIds: "") {
            totalCount
            edges {
              node {
                size
                individuals(orderBy: "full_name", businessArea: $businessArea) {
                    edges{
                        node{
                            fullName
                            phoneNo
                            documents {
                              edges {
                                node {
                                  type {
                                    type
                                  }
                                }
                              }
                            }
                            bankAccountInfo {
                              bankName
                            }
                        }
                    }
                }
              }
            }
          }
        }
        """

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("loadflexfieldsattributes")
        create_afghanistan()
        cls.business_area = BusinessArea.objects.first()
        cls.program = ProgramFactory(business_area=cls.business_area, individual_data_needed=True)
        cls.user = UserFactory()
        cls.create_user_role_with_permissions(cls.user, [Permissions.TARGETING_CREATE], cls.business_area)

    def test_golden_record_by_targeting_criteria_phone_number(self) -> None:
        create_household_and_individuals(
            {"business_area": self.business_area},
            [{"phone_no": "+48 123456789", "full_name": "individual_with_phone", "business_area": self.business_area}],
        )

        create_household_and_individuals(
            {"business_area": self.business_area},
            [{"phone_no": "", "full_name": "individual_without_phone", "business_area": self.business_area}],
        )

        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": ["True"],
                                        "fieldName": "has_phone_number",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersOtherQueryTestCase.QUERY,
            variables=variables,
        )

    def test_golden_record_by_targeting_criteria_has_bank_account_info(self) -> None:
        create_household_and_individuals(
            {"business_area": self.business_area},
            [
                {
                    "full_name": "individual_without_bank_account",
                    "phone_no": "123456789",
                    "business_area": self.business_area,
                }
            ],
        )

        _, individuals = create_household_and_individuals(
            {"business_area": self.business_area},
            [
                {
                    "full_name": "individual_with_bank_account",
                    "phone_no": "123456789",
                    "business_area": self.business_area,
                }
            ],
        )

        BankAccountInfoFactory(individual=individuals[0], bank_name="Santander")

        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": ["True"],
                                        "fieldName": "has_the_bank_account_number",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersOtherQueryTestCase.QUERY,
            variables=variables,
        )

    def test_golden_record_by_targeting_criteria_has_not_bank_account_info(self) -> None:
        create_household_and_individuals(
            {"business_area": self.business_area},
            [
                {
                    "full_name": "individual_without_bank_account",
                    "phone_no": "123456789",
                    "business_area": self.business_area,
                }
            ],
        )

        _, individuals = create_household_and_individuals(
            {"business_area": self.business_area},
            [
                {
                    "full_name": "individual_with_bank_account",
                    "phone_no": "123456789",
                    "business_area": self.business_area,
                }
            ],
        )

        BankAccountInfoFactory(individual=individuals[0], bank_name="Santander")

        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": ["False"],
                                        "fieldName": "has_the_bank_account_number",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersOtherQueryTestCase.QUERY,
            variables=variables,
        )

    def test_golden_record_by_targeting_criteria_tax_id(self) -> None:
        create_household_and_individuals(
            {"business_area": self.business_area},
            [{"full_name": "individual_without_tax_id", "phone_no": "123456789", "business_area": self.business_area}],
        )

        _, individuals = create_household_and_individuals(
            {"business_area": self.business_area},
            [{"full_name": "individual_with_tax_id", "phone_no": "123456789", "business_area": self.business_area}],
        )

        create_individual_document(individuals[0], document_type="TAX_ID")

        variables = {
            "program": self.id_to_base64(self.program.id, "Program"),
            "businessArea": self.business_area.slug,
            "targetingCriteria": {
                "rules": [
                    {
                        "filters": [],
                        "individualsFiltersBlocks": [
                            {
                                "individualBlockFilters": [
                                    {
                                        "comparisonMethod": "EQUALS",
                                        "arguments": ["True"],
                                        "fieldName": "has_tax_id_number",
                                        "isFlexField": False,
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        }
        self.snapshot_graphql_request(
            context={"user": self.user},
            request_string=GoldenRecordTargetingCriteriaWithBlockFiltersOtherQueryTestCase.QUERY,
            variables=variables,
        )
