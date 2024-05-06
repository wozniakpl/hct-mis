from typing import Any

from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse

from hct_mis_api.api.models import Grant
from hct_mis_api.api.tests.base import HOPEApiTestCase
from hct_mis_api.apps.core.fixtures import DataCollectingTypeFactory
from hct_mis_api.apps.core.models import DataCollectingType
from hct_mis_api.apps.core.utils import IDENTIFICATION_TYPE_TO_KEY_MAPPING
from hct_mis_api.apps.household.models import (
    COLLECT_TYPE_FULL,
    FEMALE,
    HEAD,
    IDENTIFICATION_TYPE_BIRTH_CERTIFICATE,
    MALE,
)
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.registration_datahub.models import (
    ImportedDocument,
    ImportedDocumentType,
    ImportedHousehold,
    ImportedIndividual,
    RegistrationDataImportDatahub,
)


class TestPushPeople(HOPEApiTestCase):
    user_permissions = [Grant.API_RDI_UPLOAD]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        ImportedDocumentType.objects.create(
            key=IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_BIRTH_CERTIFICATE], label="--"
        )
        data_collecting_type = DataCollectingTypeFactory(
            label="Full",
            code="full",
            weight=1,
            business_areas=[cls.business_area],
            type=DataCollectingType.Type.SOCIAL.value,
        )
        cls.program = ProgramFactory.create(
            status=Program.DRAFT, business_area=cls.business_area, data_collecting_type=data_collecting_type
        )
        cls.rdi = RegistrationDataImportDatahub.objects.create(
            business_area_slug=cls.business_area.slug, import_done=RegistrationDataImportDatahub.LOADING
        )
        cls.rdi2: RegistrationDataImport = RegistrationDataImport.objects.create(
            business_area=cls.business_area,
            number_of_individuals=0,
            number_of_households=0,
            datahub_id=cls.rdi.pk,
            status=RegistrationDataImport.LOADING,
            program=cls.program,
        )

        cls.url = reverse("api:rdi-push-people", args=[cls.business_area.slug, str(cls.rdi.id)])

    def test_upload_single_person(self) -> None:
        data = [
            {
                "residence_status": "IDP",
                "village": "village1",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "John Doe",
                "birth_date": "2000-01-01",
                "sex": "MALE",
                "type": "",
            }
        ]
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))
        response_json = response.json()

        rdi_datahub = RegistrationDataImportDatahub.objects.filter(id=response_json["id"]).first()
        self.assertIsNotNone(rdi_datahub)
        rdi = RegistrationDataImport.objects.filter(datahub_id=str(rdi_datahub.pk)).first()
        self.assertIsNotNone(rdi)

        self.assertEqual(rdi.program, self.program)

        hh = ImportedHousehold.objects.filter(registration_data_import=rdi_datahub).first()
        ind = ImportedIndividual.objects.filter(registration_data_import=rdi_datahub).first()
        self.assertIsNotNone(hh)
        self.assertIsNotNone(ind)
        self.assertEqual(hh.head_of_household, ind)
        self.assertEqual(hh.primary_collector, ind)
        self.assertEqual(hh.village, "village1")

        self.assertEqual(ind.full_name, "John Doe")
        self.assertEqual(ind.sex, MALE)
        self.assertEqual(ind.relationship, HEAD)

        self.assertEqual(response_json["id"], str(self.rdi.id))
        self.assertEqual(len(response_json["people"]), 1)

    def test_upload_single_person_with_documents(self) -> None:
        data = [
            {
                "residence_status": "IDP",
                "village": "village1",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "John Doe",
                "birth_date": "2000-01-01",
                "sex": "MALE",
                "type": "",
                "documents": [
                    {
                        "document_number": "10",
                        "image": "",
                        "doc_date": "2010-01-01",
                        "country": "AF",
                        "type": IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_BIRTH_CERTIFICATE],
                    }
                ],
            }
        ]
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))
        response_json = response.json()

        rdi_datahub = RegistrationDataImportDatahub.objects.filter(id=response_json["id"]).first()
        self.assertIsNotNone(rdi_datahub)

        ind = ImportedIndividual.objects.filter(registration_data_import=rdi_datahub).first()
        self.assertIsNotNone(ind)
        self.assertEqual(ind.full_name, "John Doe")
        self.assertEqual(ind.sex, MALE)

        document = ImportedDocument.objects.filter(individual=ind).first()
        self.assertIsNotNone(document)
        self.assertEqual(document.document_number, "10")

    def test_upload_multiple_people_with_documents(self) -> None:
        data = [
            {
                "residence_status": "IDP",
                "village": "village1",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "John Doe",
                "birth_date": "2000-01-01",
                "sex": "MALE",
                "type": "",
                "documents": [
                    {
                        "document_number": "10",
                        "image": "",
                        "doc_date": "2010-01-01",
                        "country": "AF",
                        "type": IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_BIRTH_CERTIFICATE],
                    }
                ],
            },
            {
                "residence_status": "IDP",
                "village": "village2",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "Mary Doe",
                "birth_date": "1990-01-01",
                "sex": "FEMALE",
                "type": "",
            },
        ]
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))
        response_json = response.json()

        rdi_datahub = RegistrationDataImportDatahub.objects.filter(id=response_json["id"]).first()
        self.assertIsNotNone(rdi_datahub)

        self.assertEqual(len(response_json["people"]), 2)

        households = ImportedHousehold.objects.filter(registration_data_import=rdi_datahub)
        self.assertEqual(len(households), 2)

        individuals = ImportedIndividual.objects.filter(registration_data_import=rdi_datahub)
        self.assertEqual(len(individuals), 2)

        john_doe = ImportedIndividual.objects.filter(full_name="John Doe").first()

        self.assertIsNotNone(john_doe)
        self.assertEqual(john_doe.full_name, "John Doe")
        self.assertEqual(john_doe.sex, MALE)

        mary_doe = ImportedIndividual.objects.filter(full_name="Mary Doe").first()

        self.assertIsNotNone(mary_doe)
        self.assertEqual(mary_doe.full_name, "Mary Doe")
        self.assertEqual(mary_doe.sex, FEMALE)

        document = ImportedDocument.objects.filter(individual=john_doe).first()
        self.assertIsNotNone(document)
        self.assertEqual(document.document_number, "10")

    def test_upload_with_errors(self) -> None:
        data = [
            {
                "residence_status": "IDP",
                "country": "AF",
                "full_name": "John Doe",
                "sex": "MALE",
                "documents": [
                    {
                        "image": "",
                        "country": "AF",
                    }
                ],
            },
            {
                "residence_status": "IDP",
                "village": "village2",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "Mary Doe",
                "sex": "FEMALE",
            },
        ]
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, str(response.json()))
        self.assertEqual(
            response.json(),
            [
                {
                    "birth_date": ["This field is required."],
                    "collect_individual_data": ["This field is required."],
                    "documents": [
                        {
                            "doc_date": ["This field is required."],
                            "document_number": ["This field is required."],
                            "type": ["This field is required."],
                        }
                    ],
                    "type": ["This field is required."],
                },
                {"birth_date": ["This field is required."], "type": ["This field is required."]},
            ],
        )

    @parameterized.expand(
        [
            ("invalid_phone_no", "phone_no", "invalid", False),
            ("invalid_phone_no_alternative", "phone_no", "invalid", False),
            ("valid_phone_no", "phone_no_alternative", "+48 632 215 789", True),
            ("valid_phone_no_alternative", "phone_no_alternative", "+48 632 215 789", True),
        ]
    )
    def test_upload_single_person_with_phone_number(
        self, _: Any, field_name: str, phone_number: str, expected_value: bool
    ) -> None:
        data = [
            {
                "residence_status": "IDP",
                "village": "village1",
                "country": "AF",
                "collect_individual_data": COLLECT_TYPE_FULL,
                "full_name": "John Doe",
                "birth_date": "2000-01-01",
                "sex": "MALE",
                "type": "",
                field_name: phone_number,
            }
        ]
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))
        response_json = response.json()

        rdi_datahub = RegistrationDataImportDatahub.objects.filter(id=response_json["id"]).first()
        self.assertIsNotNone(rdi_datahub)
        ind = ImportedIndividual.objects.filter(registration_data_import=rdi_datahub).first()
        self.assertIsNotNone(ind)
        self.assertEqual(ind.full_name, "John Doe")
        self.assertEqual(getattr(ind, f"{field_name}_valid"), expected_value)
