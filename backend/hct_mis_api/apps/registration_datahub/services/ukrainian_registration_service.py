import json
from typing import List

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.forms import modelform_factory

from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.core.utils import build_arg_dict_from_dict
from hct_mis_api.apps.household.models import (
    IDENTIFICATION_TYPE_BIRTH_CERTIFICATE,
    IDENTIFICATION_TYPE_DRIVERS_LICENSE,
    IDENTIFICATION_TYPE_NATIONAL_ID,
    IDENTIFICATION_TYPE_NATIONAL_PASSPORT,
    IDENTIFICATION_TYPE_RESIDENCE_PERMIT_NO,
    IDENTIFICATION_TYPE_TAX_ID,
    DISABLED,
    NOT_DISABLED,
    ROLE_PRIMARY,
    BankAccountInfo,
    ROLE_ALTERNATE,
)
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.registration_datahub.models import (
    ImportData,
    ImportedDocument,
    ImportedDocumentType,
    ImportedHousehold,
    ImportedIndividual,
    Record,
    RegistrationDataImportDatahub,
    ImportedIndividualRoleInHousehold,
)


class UkrainianRegistrationService:
    INDIVIDUAL_MAPPING_DICT = {
        "given_name_i_c": "given_name",
        "family_name_i_c": "family_name",
        "patronymic": "middle_name",
        "birth_date": "birth_date",
        "gender_i_c": "sex",
        "relationship_i_c": "relationship",
        "disability_i_c": "disability",
        # "disabiliyt_recognize_i_c": "disability_recognize",
        # "disability_certificate_picture": "disability_certificate_picture",
        "phone_no_i_c": "phone_no",
        "role_i_c": "role",
    }

    HOUSEHOLD_MAPPING_DICT = {
        "residence_status": "residence_status_h_c",
        "admin1_h_c": "admin1",
        "admin2_h_c": "admin2",
        "admin3_h_c": "admin3",
        "size": "size_h_c",
        # "where_are_you_now": "",
    }
    DOCUMENT_MAPPING_TYPE_DICT = {
        "national_id_no_i_c_1": IDENTIFICATION_TYPE_NATIONAL_ID,
        "international_passport_i_c": IDENTIFICATION_TYPE_NATIONAL_PASSPORT,
        "drivers_license_no_i_c": IDENTIFICATION_TYPE_DRIVERS_LICENSE,
        "birth_certificate_no_i_c": IDENTIFICATION_TYPE_BIRTH_CERTIFICATE,
        "residence_permit_no_i_c": IDENTIFICATION_TYPE_RESIDENCE_PERMIT_NO,
        "tax_id_no_i_c": IDENTIFICATION_TYPE_TAX_ID,
        # "national_id_picture": "photo",
        # "international_passport_picture": "photo",
        # "drivers_license_picture": "photo",
        # "birth_certificate_picture": "photo",
        # "residence_permit_picture": "photo",
        # "tax_id_picture": "photo",
    }

    def __init__(self, records: QuerySet[Record]):
        self.records = records

    @atomic("default")
    @atomic("registration_datahub")
    def create_rdi(self, imported_by, rdi_name="rdi_name"):
        business_area = BusinessArea.objects.get(slug="ukraine")
        number_of_individuals = 0
        number_of_households = self.records.count()

        rdi = RegistrationDataImport.objects.create(
            name=rdi_name,
            data_source=RegistrationDataImport.FLEX_REGISTRATION,
            imported_by=imported_by,
            number_of_individuals=number_of_individuals,
            number_of_households=number_of_households,
            business_area=business_area,
            status=RegistrationDataImport.IMPORTING,
        )

        import_data = ImportData.objects.create(
            status=ImportData.STATUS_PENDING,
            business_area_slug=business_area.slug,
            data_type=ImportData.FLEX_REGISTRATION,
            number_of_individuals=number_of_individuals,
            number_of_households=number_of_households,
            created_by_id=imported_by.id,
        )
        rdi_datahub = RegistrationDataImportDatahub.objects.create(
            name=rdi_name,
            hct_id=rdi.id,
            import_data=import_data,
            import_done=RegistrationDataImportDatahub.NOT_STARTED,
            business_area_slug=business_area.slug,
        )

        for record in self.records:
            number_of_individuals += self.create_household_for_rdi_household(record, rdi_datahub)

        rdi.number_of_individuals = number_of_individuals
        import_data.number_of_individuals = number_of_individuals

        rdi.save(update_fields=("number_of_individuals",))
        import_data.save(update_fields=("number_of_individuals",))

    def create_household_for_rdi_household(
        self, record: Record, registration_data_import: RegistrationDataImportDatahub
    ):
        individuals: List[ImportedIndividual] = []
        documents: List[ImportedDocument] = []
        record_data_dict = json.loads(record.storage.tobytes().decode("utf-8"))
        household_dict = record_data_dict.get("household", [])[0]
        individuals_array = record_data_dict.get("individuals", [])

        self.validate_household(individuals_array)

        household_data = self._prepare_household_data(household_dict, record, registration_data_import)
        household = self._create_object_and_validate(household_data, ImportedHousehold)

        for individual_dict in individuals_array:
            individual_data = self._prepare_individual_data(individual_dict, household, registration_data_import)
            role = individual_data.pop("role")
            individual = self._create_object_and_validate(individual_data, ImportedIndividual)
            bank_account_data = self._prepare_bank_account_info(individual_dict, individual)
            individual = self._create_object_and_validate(bank_account_data, BankAccountInfo)
            self._create_role(role, individual, household)
            individuals.append(individual)

            documents.extend(self._prepare_documents(individual_dict, individual))

        record.registration_data_import = registration_data_import
        record.save(update_fields=("registration_data_import",))
        ImportedDocument.objects.bulk_create(documents)
        return len(individuals)

    def _create_role(self, role, individual, household):
        if role == "y":
            defaults = dict(individual=individual, household=household)
            if ImportedIndividualRoleInHousehold.objects.filter(household=household, role=ROLE_PRIMARY).count() == 0:
                ImportedIndividualRoleInHousehold.objects.create(**defaults, role=ROLE_PRIMARY)
            elif (
                ImportedIndividualRoleInHousehold.objects.filter(household=household, role=ROLE_ALTERNATE).count() == 0
            ):
                ImportedIndividualRoleInHousehold.objects.create(**defaults, role=ROLE_ALTERNATE)
            else:
                raise ValidationError("There should be only two collectors!")

    def _create_object_and_validate(self, data, model_class):
        ModelClassForm = modelform_factory(model_class, fields=data.keys())
        form = ModelClassForm(data)
        if not form.is_valid():
            raise ValidationError(form.errors)
        return form.save()

    def _prepare_household_data(self, household_dict, record, registration_data_import) -> dict:
        return dict(
            **build_arg_dict_from_dict(household_dict, UkrainianRegistrationService.HOUSEHOLD_MAPPING_DICT),
            flex_registrations_record=record,
            registration_data_import=registration_data_import,
        )

    def _prepare_individual_data(
        self,
        individual_dict: dict,
        household: ImportedHousehold,
        registration_data_import: RegistrationDataImportDatahub,
    ) -> dict:
        individual_data = dict(
            **build_arg_dict_from_dict(individual_dict, UkrainianRegistrationService.HOUSEHOLD_MAPPING_DICT),
            household=household,
            registration_data_import=registration_data_import,
        )
        if disability := individual_data.get("disability"):
            if disability == "y":
                individual_data["disability"] = DISABLED
            else:
                individual_data["disability"] = NOT_DISABLED

        if relationship := individual_data.get("relationship"):
            individual_data["relationship"] = relationship.upper()

        return individual_data

    def _prepare_documents(self, individual_dict: dict, individual: ImportedIndividual) -> List[ImportedDocument]:
        documents = []
        for field_name, document_type_string in UkrainianRegistrationService.DOCUMENT_MAPPING_TYPE_DICT:
            document_number = individual_dict.get(field_name)
            if not document_number:
                continue
            document_type = ImportedDocumentType.objects.get(type=document_type_string, country="UA")
            documents.append(
                ImportedDocument(document_type=document_type, document_number=document_number, individual=individual)
            )
        return documents

    def _prepare_bank_account_info(self, individual_dict: dict, individual: ImportedIndividual):
        if individual_dict.get("bank_account_h_f", "n") != "y":
            return
        bank_name = individual_dict.get("bank_name_h_f", "")
        other_bank_name = individual_dict.get("other_bank_name", "")
        if not bank_name:
            bank_name = other_bank_name
        bank_account_info_data = {
            "bank_account_number": individual_dict.get("bank_account_number", ""),
            "bank_name": bank_name,
            "debit_card_number": individual_dict.get("bank_account_number", ""),
            "individual": individual,
        }
        return bank_account_info_data

    def validate_household(self, individuals_array):
        if not individuals_array:
            raise ValidationError("Household should has at least one individual")
