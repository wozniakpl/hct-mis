from typing import Any
from unittest.mock import patch

from hct_mis_api.apps.account.fixtures import PartnerFactory
from hct_mis_api.apps.core.base_test_case import BaseElasticSearchTestCase
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.geo.fixtures import AreaFactory, CountryFactory
from hct_mis_api.apps.household.fixtures import (
    BankAccountInfoFactory,
    DocumentFactory,
    DocumentTypeFactory,
    IndividualIdentityFactory,
    IndividualRoleInHouseholdFactory,
    create_household_and_individuals,
)
from hct_mis_api.apps.household.models import (
    HEAD,
    MALE,
    ROLE_PRIMARY,
    BankAccountInfo,
    Document,
    Household,
    Individual,
    IndividualIdentity,
    IndividualRoleInHousehold,
)
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.registration_data.fixtures import (
    RegistrationDataImportDatahubFactory,
    RegistrationDataImportFactory,
)
from hct_mis_api.apps.registration_data.models import (
    RegistrationDataImport,
    RegistrationDataImportDatahub,
)
from hct_mis_api.apps.registration_datahub.celery_tasks import (
    registration_program_population_import_task,
)


class TestRegistrationProgramPopulationImportTask(BaseElasticSearchTestCase):
    databases = {"default", "registration_datahub"}

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.afghanistan = create_afghanistan()
        country = CountryFactory()
        cls.program_from = ProgramFactory(business_area=cls.afghanistan)
        cls.program_to = ProgramFactory(business_area=cls.afghanistan)
        cls.registration_data_import = RegistrationDataImportFactory(
            business_area=cls.afghanistan,
            program=cls.program_to,
        )
        cls.rdi_other = RegistrationDataImportFactory(
            business_area=cls.afghanistan,
            program=cls.program_from,
        )
        cls.registration_data_import_datahub = RegistrationDataImportDatahubFactory(
            business_area_slug=cls.afghanistan.slug,
            hct_id=cls.registration_data_import.id,
        )
        cls.registration_data_import.datahub_id = cls.registration_data_import_datahub.id
        cls.registration_data_import.save()

        cls.household, cls.individuals = create_household_and_individuals(
            household_data={
                "registration_data_import": cls.rdi_other,
                "program": cls.program_from,
                "admin_area": AreaFactory(),
                "admin1": AreaFactory(),
                "admin2": AreaFactory(),
                "admin3": AreaFactory(),
                "admin4": AreaFactory(),
                "registration_id": "1234567890",
                "flex_fields": {"enumerator_id": "123", "some": "thing"},
            },
            individuals_data=[
                {
                    "registration_data_import": cls.rdi_other,
                    "given_name": "Test",
                    "full_name": "Test Testowski",
                    "middle_name": "",
                    "family_name": "Testowski",
                    "phone_no": "123-123-123",
                    "phone_no_alternative": "",
                    "relationship": HEAD,
                    "sex": MALE,
                    "birth_date": "1955-09-07",
                },
                {},
            ],
        )
        cls.ind_role_in_hh = IndividualRoleInHouseholdFactory(
            household=cls.household,
            individual=cls.individuals[1],
            role=ROLE_PRIMARY,
        )
        document_type = DocumentTypeFactory(key="birth_certificate")
        DocumentTypeFactory(
            key=document_type.key,
        )
        cls.document = DocumentFactory(
            individual=cls.individuals[0],
            program=cls.program_from,
            type=document_type,
            country=country,
        )
        cls.identity = IndividualIdentityFactory(
            individual=cls.individuals[0],
            country=country,
            partner=PartnerFactory(),
        )

        cls.bank_account_info = BankAccountInfoFactory(
            individual=cls.individuals[0],
        )

    def _run_task(self) -> None:
        registration_program_population_import_task(
            str(self.registration_data_import_datahub.id),
            str(self.afghanistan.id),
            str(self.program_from.id),
            str(self.program_to.id),
        )

    def _imported_objects_count_before(self) -> None:
        self.assertEqual(
            Household.pending_objects.filter().count(),
            0,
        )
        self.assertEqual(
            Individual.pending_objects.count(),
            0,
        )
        self.assertEqual(
            IndividualIdentity.pending_objects.count(),
            0,
        )
        self.assertEqual(
            Document.pending_objects.count(),
            0,
        )
        self.assertEqual(
            BankAccountInfo.pending_objects.count(),
            0,
        )
        self.assertEqual(
            IndividualRoleInHousehold.pending_objects.count(),
            0,
        )

    def _imported_objects_count_after(self, multiplier: int = 1) -> None:
        self.assertEqual(
            Household.pending_objects.count(),
            1 * multiplier,
        )
        self.assertEqual(
            Individual.pending_objects.count(),
            2 * multiplier,
        )
        self.assertEqual(
            IndividualIdentity.pending_objects.count(),
            1 * multiplier,
        )
        self.assertEqual(
            Document.pending_objects.count(),
            1 * multiplier,
        )
        self.assertEqual(
            BankAccountInfo.pending_objects.count(),
            1 * multiplier,
        )
        self.assertEqual(
            IndividualRoleInHousehold.pending_objects.count(),
            1 * multiplier,
        )

    def test_registration_program_population_import_task_wrong_status(self) -> None:
        rdi_status = self.registration_data_import.status
        self._run_task()
        self.registration_data_import.refresh_from_db()
        self.assertEqual(
            rdi_status,
            self.registration_data_import.status,
        )

    def test_registration_program_population_import_task(self) -> None:
        self.registration_data_import.status = RegistrationDataImport.IMPORT_SCHEDULED
        self.registration_data_import.save()

        self._imported_objects_count_before()

        self._run_task()

        self.registration_data_import.refresh_from_db()
        self.assertEqual(
            self.registration_data_import.status,
            RegistrationDataImport.IN_REVIEW,
        )
        self.registration_data_import_datahub.refresh_from_db()
        self.assertEqual(
            self.registration_data_import_datahub.import_done,
            RegistrationDataImportDatahub.DONE,
        )

        self._imported_objects_count_after()

        registration_data_import2 = RegistrationDataImportFactory(
            name="Other",
            status=RegistrationDataImport.IMPORT_SCHEDULED,
            business_area=self.afghanistan,
            program=self.program_to,
        )

        registration_data_import_datahub2 = RegistrationDataImportDatahubFactory(
            business_area_slug=self.afghanistan.slug,
            hct_id=registration_data_import2.id,
        )
        registration_data_import2.datahub_id = registration_data_import_datahub2.id
        registration_data_import2.save()

        registration_program_population_import_task(
            str(registration_data_import_datahub2.id),
            str(self.afghanistan.id),
            str(self.program_from.id),
            str(self.program_to.id),
        )
        self._imported_objects_count_after(2)

    def test_registration_program_population_import_task_error(self) -> None:
        self.registration_data_import.delete()
        with self.assertRaises(RegistrationDataImport.DoesNotExist):
            self._run_task()

        self.registration_data_import_datahub.refresh_from_db()
        self.assertEqual(
            self.registration_data_import_datahub.import_done,
            RegistrationDataImportDatahub.DONE,
        )

    def test_registration_program_population_import_ba_postpone_deduplication(self) -> None:
        self.afghanistan.postpone_deduplication = True
        self.afghanistan.save()
        self.registration_data_import.status = RegistrationDataImport.IMPORT_SCHEDULED
        self.registration_data_import.save()

        self._run_task()

        self.registration_data_import.refresh_from_db()
        self.assertEqual(
            self.registration_data_import.status,
            RegistrationDataImport.IN_REVIEW,
        )

    @patch("hct_mis_api.apps.registration_datahub.celery_tasks.locked_cache")
    def test_registration_program_population_import_locked_cache(self, mocked_locked_cache: Any) -> None:
        mocked_locked_cache.return_value.__enter__.return_value = False
        self.registration_data_import.status = RegistrationDataImport.IMPORT_SCHEDULED
        self.registration_data_import.save()

        self._run_task()

        self.registration_data_import.refresh_from_db()
        self.assertEqual(
            self.registration_data_import.status,
            RegistrationDataImport.IMPORT_SCHEDULED,
        )
