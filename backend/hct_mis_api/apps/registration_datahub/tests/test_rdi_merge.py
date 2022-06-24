from django.forms import model_to_dict

from hct_mis_api.apps.household.models import Individual, Household, HEAD, COUSIN, BROTHER_SISTER, YES
from hct_mis_api.apps.registration_data.fixtures import RegistrationDataImportFactory
from hct_mis_api.apps.registration_datahub.fixtures import (
    RegistrationDataImportDatahubFactory,
    ImportedHouseholdFactory,
    ImportedIndividualFactory,
)
from hct_mis_api.apps.core.base_test_case import BaseElasticSearchTestCase

from freezegun import freeze_time


class TestRdiMergeTask(BaseElasticSearchTestCase):
    databases = "__all__"
    fixtures = [
        "hct_mis_api/apps/core/fixtures/data.json",
    ]

    @classmethod
    def setUpTestData(cls):
        from hct_mis_api.apps.registration_datahub.tasks.rdi_merge import RdiMergeTask

        cls.RdiMergeTask = RdiMergeTask

        cls.rdi = RegistrationDataImportFactory()
        rdi_hub = RegistrationDataImportDatahubFactory(
            name=cls.rdi.name, hct_id=cls.rdi.id, business_area_slug=cls.rdi.business_area.slug
        )
        cls.rdi.datahub_id = rdi_hub.id
        cls.rdi.save()

        imported_household = ImportedHouseholdFactory(
            collect_individual_data=YES,
            registration_data_import=rdi_hub,
        )

        individuals_to_create = [
            {
                "full_name": "Benjamin Butler",
                "given_name": "Benjamin",
                "family_name": "Butler",
                "relationship": HEAD,
                "birth_date": "1962-02-02",  # age 39
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Robin Ford",
                "given_name": "Robin",
                "family_name": "Ford",
                "relationship": COUSIN,
                "birth_date": "2017-02-15",  # age 4
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Timothy Perry",
                "given_name": "Timothy",
                "family_name": "Perry",
                "relationship": COUSIN,
                "birth_date": "2011-12-21",  # age 10
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Eric Torres",
                "given_name": "Eric",
                "family_name": "Torres",
                "relationship": BROTHER_SISTER,
                "birth_date": "2006-03-23",  # age 15
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Baz Bush",
                "given_name": "Baz",
                "family_name": "Bush",
                "relationship": BROTHER_SISTER,
                "birth_date": "2005-02-21",  # age 16
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Liz Female",
                "given_name": "Liz",
                "family_name": "Female",
                "relationship": BROTHER_SISTER,
                "birth_date": "2005-10-10",  # age 16
                "sex": "FEMALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Jenna Franklin",
                "given_name": "Jenna",
                "family_name": "Franklin",
                "relationship": BROTHER_SISTER,
                "birth_date": "1996-11-29",  # age 25
                "sex": "FEMALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
            {
                "full_name": "Bob Jackson",
                "given_name": "Bob",
                "family_name": "Jackson",
                "relationship": BROTHER_SISTER,
                "birth_date": "1956-03-03",  # age 65
                "sex": "MALE",
                "registration_data_import": rdi_hub,
                "household": imported_household,
            },
        ]

        cls.individuals = [ImportedIndividualFactory(**individual) for individual in individuals_to_create]

    @freeze_time("2022-01-01")
    def test_merge_rdi_and_recalculation(self):
        self.RdiMergeTask().execute(self.rdi.pk)

        households = Household.objects.all()
        individuals = Individual.objects.all()

        self.assertEqual(1, households.count())
        self.assertEqual(8, individuals.count())

        household_data = model_to_dict(
            households[0],
            (
                "female_age_group_0_5_count",
                "female_age_group_6_11_count",
                "female_age_group_12_17_count",
                "female_age_group_18_59_count",
                "female_age_group_60_count",
                "male_age_group_0_5_count",
                "male_age_group_6_11_count",
                "male_age_group_12_17_count",
                "male_age_group_18_59_count",
                "male_age_group_60_count",
                "children_count",
            ),
        )

        expected = {
            "female_age_group_0_5_count": 0,
            "female_age_group_6_11_count": 0,
            "female_age_group_12_17_count": 1,
            "female_age_group_18_59_count": 1,
            "female_age_group_60_count": 0,
            "male_age_group_0_5_count": 1,
            "male_age_group_6_11_count": 1,
            "male_age_group_12_17_count": 2,
            "male_age_group_18_59_count": 1,
            "male_age_group_60_count": 1,
            "children_count": 5,
        }
        self.assertEqual(household_data, expected)
