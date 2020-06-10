from functools import reduce

from core.countries import Countries
from core.models import AdminArea

from core.utils import (
    age_to_birth_date_query,
    LazyEvalMethodsDict,
)
from household.models import (
    RESIDENCE_STATUS_CHOICE,
    RELATIONSHIP_CHOICE,
    ROLE_CHOICE,
    SEX_CHOICE,
    MARITAL_STATUS_CHOICE,
)

TYPE_ID = "ID"
TYPE_INTEGER = "INTEGER"
TYPE_STRING = "STRING"
TYPE_BOOL = "BOOL"
TYPE_DATE = "DATE"
TYPE_IMAGE = "IMAGE"
TYPE_SELECT_ONE = "SELECT_ONE"
TYPE_SELECT_MANY = "SELECT_MANY"
TYPE_GEOPOINT = "GEOPOINT"

_INDIVIDUAL = "Individual"
_HOUSEHOLD = "Household"

FILTERABLE_TYPES = [
    TYPE_INTEGER,
    TYPE_STRING,
    TYPE_SELECT_ONE,
    TYPE_SELECT_MANY,
]

CORE_FIELDS_ATTRIBUTES = [
    {
        "id": "a1741e3c-0e24-4a60-8d2f-463943abaebb",
        "type": TYPE_INTEGER,
        "name": "age",
        "label": {"English(EN)": "Age (calculated)"},
        "hint": "",
        "required": False,
        "get_query": age_to_birth_date_query,
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "age",
    },
    {
        "id": "3c2473d6-1e81-4025-86c7-e8036dd92f4b",
        "type": TYPE_SELECT_ONE,
        "name": "residence_status",
        "lookup": "residence_status",
        "required": True,
        "label": {"English(EN)": "Residence status"},
        "hint": "",
        "choices": [
            {"label": {"English(EN)": label}, "value": value,}
            for value, label in RESIDENCE_STATUS_CHOICE
        ],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "residence_status_h_c",
    },
    {
        "id": "e47bafa7-0b86-4be9-a07f-d3fc7ac698cf",
        "type": TYPE_IMAGE,
        "name": "consent",
        "lookup": "consent",
        "required": True,
        "label": {"English(EN)": "Do you consent?"},
        "hint": "image of consent",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "consent_h_c",
    },
    {
        "id": "e44efed6-47d6-4f60-bcf6-b1d2ffc4d7d1",
        "type": TYPE_SELECT_ONE,
        "name": "country_origin",
        "lookup": "country_origin",
        "required": False,
        "label": {"English(EN)": "Country origin"},
        "hint": "country origin",
        "choices": Countries.get_choices(),
        "custom_validate_choices": Countries.is_valid_country_choice,
        "custom_cast_value": Countries.get_country_value,
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "country_origin_h_c",
    },
    {
        "id": "aa79985c-b616-453c-9884-0666252c3070",
        "type": TYPE_SELECT_ONE,
        "name": "country",
        "lookup": "country",
        "required": False,
        "label": {"English(EN)": "Country"},
        "hint": "",
        "choices": Countries.get_choices(),
        "custom_validate_choices": Countries.is_valid_country_choice,
        "custom_cast_value": Countries.get_country_value,
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "country_h_c",
    },
    {
        "id": "59685cec-69bf-4abe-81b4-70b8f05b89f3",
        "type": TYPE_STRING,
        "name": "address",
        "lookup": "address",
        "required": False,
        "label": {"English(EN)": "Address"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "address_h_c",
    },
    LazyEvalMethodsDict(
        {
            "id": "c53ea58b-e7cf-4bf3-82d0-dec41f66ef3a",
            "type": TYPE_SELECT_ONE,
            "name": "admin1",
            "lookup": "admin1",
            "required": False,
            "label": {
                "English(EN)": "Household resides in (Select administrative level 1)"
            },
            "hint": "",
            "choices": lambda: AdminArea.get_admin_areas_as_choices(1),
            "associated_with": _HOUSEHOLD,
            "xlsx_field": "admin1_h_c",
        }
    ),
    LazyEvalMethodsDict(
        {
            "id": "e4eb6632-8204-44ed-b39c-fe791ded9246",
            "type": TYPE_SELECT_ONE,
            "name": "admin2",
            "lookup": "admin2",
            "required": False,
            "label": {
                "English(EN)": "Household resides in (Select administrative level 2)"
            },
            "hint": "",
            "choices": lambda: AdminArea.get_admin_areas_as_choices(2),
            "associated_with": _HOUSEHOLD,
            "xlsx_field": "admin2_h_c",
        }
    ),
    {
        "id": "13a9d8b0-f278-47c2-9b1b-b06579b0ab35",
        "type": TYPE_GEOPOINT,
        "name": "geopoint",
        "lookup": "geopoint",
        "required": False,
        "label": {"English(EN)": "Household Geopoint"},
        "hint": "latitude and longitude of household",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "hh_geopoint_h_c",
    },
    {
        "id": "5b32bad5-ff7c-4e6b-af7e-a0287fe91ea2",
        "type": TYPE_STRING,
        "name": "unhcr_id",
        "lookup": "unhcr_id",
        "required": False,
        "label": {"English(EN)": "UNHCR Case ID"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "unhcr_hh_id_h_c",
    },
    {
        "id": "5f530642-b889-4130-bf1a-5fac1b17cf09",
        "type": TYPE_BOOL,
        "name": "returnee",
        "lookup": "returnee",
        "required": False,
        "label": {"English(EN)": "Is this a returnee household?"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "returnee_h_c",
    },
    {
        "id": "d668ae31-12cf-418e-8f7f-4c6398d82ffd",
        "type": TYPE_INTEGER,
        "name": "size",
        "lookup": "size",
        "required": True,
        "label": {"English(EN)": "What is the household size?"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "size_h_c",
    },
    {
        "id": "8d9df01a-ce7c-4e78-b8ec-6f3eec8f30ce",
        "type": TYPE_SELECT_ONE,
        "name": "relationship",
        "lookup": "relationship",
        "required": True,
        "label": {"English(EN)": "Relationship to Head of Household"},
        "hint": "",
        "choices": [
            {"label": {"English(EN)": label}, "value": value,}
            for value, label in RELATIONSHIP_CHOICE
        ],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "relationship_i_c",
    },
    {
        "id": "f72eea9e-aaca-4085-93ff-9d194143d354",
        "type": TYPE_SELECT_ONE,
        "name": "role",
        "lookup": "role",
        "required": False,
        "label": {"English(EN)": "Role"},
        "hint": "",
        "choices": [
            {"label": {"English(EN)": label}, "value": value,}
            for value, label in ROLE_CHOICE
        ],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "role_i_c",
    },
    {
        "id": "36ab3421-6e7a-40d1-b816-ea5cbdcc0b6a",
        "type": TYPE_STRING,
        "name": "full_name",
        "lookup": "full_name",
        "required": True,
        "label": {"English(EN)": "Full Name"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "full_name_i_c",
    },
    {
        "id": "b1f90314-b8b8-4bcb-9265-9d48d1fce5a4",
        "type": TYPE_STRING,
        "name": "given_name",
        "lookup": "given_name",
        "required": False,
        "label": {"English(EN)": "Given Name"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "given_name_i_c",
    },
    {
        "id": "6f603107-bd88-4a8d-97cc-748a7238358d",
        "type": TYPE_STRING,
        "name": "middle_name",
        "lookup": "middle_name",
        "required": False,
        "label": {"English(EN)": "Middle Names"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "middle_name_i_c",
    },
    {
        "id": "3f74dd36-bfd2-4c84-bfc7-21f7adbff7f0",
        "type": TYPE_STRING,
        "name": "family_name",
        "lookup": "family_name",
        "required": False,
        "label": {"English(EN)": "Family Name"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "family_name_i_c",
    },
    {
        "id": "da726870-dfc9-48dc-aba9-b9138b611c74",
        "type": TYPE_SELECT_ONE,
        "name": "sex",
        "lookup": "sex",
        "required": True,
        "label": {"English(EN)": "Sex"},
        "hint": "",
        "choices": [
            {"label": {"English(EN)": label}, "value": value,}
            for value, label in SEX_CHOICE
        ],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "sex_i_c",
    },
    {
        "id": "416b0119-2d89-4517-819d-e563d2eb428c",
        "type": TYPE_DATE,
        "name": "birth_date",
        "lookup": "birth_date",
        "required": True,
        "label": {"English(EN)": "Birth Date"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "birth_date_i_c",
    },
    {
        "id": "5e2c2a7c-9651-4c07-873c-f594ae18a56a",
        "type": TYPE_BOOL,
        "name": "estimated_birth_date",
        "lookup": "estimated_birth_date",
        "required": False,
        "label": {"English(EN)": "Estimated Birth Date?"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "estimated_birth_date_i_c",
    },
    {
        "id": "84827966-17e5-407a-9424-1350c7ec3b64",
        "type": TYPE_IMAGE,
        "name": "photo",
        "lookup": "photo",
        "required": False,
        "label": {"English(EN)": "Photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "photo_i_c",
    },
    {
        "id": "35ede8c4-877e-40dc-a93a-0a9a3bc511dc",
        "type": TYPE_SELECT_ONE,
        "name": "marital_status",
        "lookup": "marital_status",
        "required": True,
        "label": {"English(EN)": "Marital Status"},
        "hint": "",
        "choices": [
            {"label": {"English(EN)": label}, "value": value,}
            for value, label in MARITAL_STATUS_CHOICE
        ],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "marital_status_i_c",
    },
    {
        "id": "01c1ae70-d8f8-4451-96c5-09afb4ff3057",
        "type": TYPE_STRING,
        "name": "phone_no",
        "lookup": "phone_no",
        "required": False,
        "label": {"English(EN)": "Phone number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "phone_no_i_c",
    },
    {
        "id": "f7609980-95c4-4b18-82dc-132a04ce7d65",
        "type": TYPE_STRING,
        "name": "phone_no_alternative",
        "lookup": "phone_no_alternative",
        "required": False,
        "label": {"English(EN)": "Alternative phone number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "phone_no_alternative_i_c",
    },
    {
        "id": "f1d0c0c1-53d7-422a-be3d-b3588ee0ff58",
        "type": TYPE_STRING,
        "name": "birth_certificate_no",
        "lookup": "birth_certificate_no",
        "required": False,
        "label": {"English(EN)": "Birth certificate number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "birth_certificate_no_i_c",
    },
    {
        "id": "12ceb917-8942-4cb6-a9d0-6a97a097258a",
        "type": TYPE_IMAGE,
        "name": "birth_certificate_photo",
        "lookup": "birth_certificate_photo",
        "required": False,
        "label": {"English(EN)": "Birth certificate photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "birth_certificate_photo_i_c",
    },
    {
        "id": "34a9519f-9c42-4910-b097-157ec8e6e31f",
        "type": TYPE_STRING,
        "name": "drivers_license_no",
        "lookup": "drivers_license_no",
        "required": False,
        "label": {"English(EN)": "Driver's license number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "drivers_license_no_i_c",
    },
    {
        "id": "7e6a41c5-0fbd-4f99-98ba-2c6a7da8dbe4",
        "type": TYPE_IMAGE,
        "name": "drivers_license_photo",
        "lookup": "drivers_license_photo",
        "required": False,
        "label": {"English(EN)": "Driver's license photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "drivers_license_photo_i_c",
    },
    {
        "id": "225832fc-c61b-4100-aac9-352d272d15fd",
        "type": TYPE_STRING,
        "name": "electoral_card_no",
        "lookup": "electoral_card_no",
        "required": False,
        "label": {"English(EN)": "Electoral card number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "electoral_card_no_i_c",
    },
    {
        "id": "ffb6a487-a806-47d6-a12f-fe3c6c516976",
        "type": TYPE_IMAGE,
        "name": "electoral_card_photo",
        "lookup": "electoral_card_photo",
        "required": False,
        "label": {"English(EN)": "Electoral card photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "electoral_card_photo_i_c",
    },
    {
        "id": "1c7f6c85-1621-48f1-88f3-a172d69aa316",
        "type": TYPE_STRING,
        "name": "unhcr_id_no",
        "lookup": "unhcr_id_no",
        "required": False,
        "label": {"English(EN)": "UNHCR ID number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "unhcr_id_no_i_c",
    },
    {
        "id": "2f9ca147-afde-4311-9d61-e906a8ef2334",
        "type": TYPE_IMAGE,
        "name": "unhcr_id_photo",
        "lookup": "unhcr_id_photo",
        "required": False,
        "label": {"English(EN)": "UNHCR ID photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "unhcr_id_photo_i_c",
    },
    {
        "id": "4e836832-2cf2-4073-80eb-21316eaf7277",
        "type": TYPE_STRING,
        "name": "national_passport",
        "lookup": "national_passport",
        "required": False,
        "label": {"English(EN)": "National passport number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "national_passport_i_c",
    },
    {
        "id": "234a1b5b-7900-4f67-86a9-5fcaede3d09d",
        "type": TYPE_IMAGE,
        "name": "national_passport_photo",
        "lookup": "national_passport_photo",
        "required": False,
        "label": {"English(EN)": "National passport photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "national_passport_photo_i_c",
    },
    {
        "id": "eff20a18-4336-4273-bbb8-ed0e9a94ebbb",
        "type": TYPE_STRING,
        "name": "national_id",
        "lookup": "national_id",
        "required": False,
        "label": {"English(EN)": "National ID number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "national_id_i_c",
    },
    {
        "id": "d43304d9-91e4-4317-9356-f7066b898b16",
        "type": TYPE_IMAGE,
        "name": "national_id_photo",
        "lookup": "national_id_photo",
        "required": False,
        "label": {"English(EN)": "National ID photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "national_id_photo_i_c",
    },
    {
        "id": "201c91d2-8f89-46c9-ba5a-db7130140402",
        "type": TYPE_STRING,
        "name": "scope_id_no",
        "lookup": "scope_id_no",
        "required": False,
        "label": {"English(EN)": "WFP Scope ID number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "scope_id_no_i_c",
    },
    {
        "id": "4aa3d595-131a-48df-8752-ec171eabe3be",
        "type": TYPE_IMAGE,
        "name": "scope_id_photo",
        "lookup": "scope_id_photo",
        "required": False,
        "label": {"English(EN)": "WFP Scope ID photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "scope_id_photo_i_c",
    },
    {
        "id": "3bf6105f-87d0-479b-bf92-7f90af4d8462",
        "type": TYPE_STRING,
        "name": "other_id_type",
        "lookup": "other_id_type",
        "required": False,
        "label": {"English(EN)": "If other type of ID, specify the type"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "other_id_type_i_c",
    },
    {
        "id": "556e14af-9901-47f3-bf2c-20b4c721e8f7",
        "type": TYPE_STRING,
        "name": "other_id_no",
        "lookup": "other_id_no",
        "required": False,
        "label": {"English(EN)": "ID number"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "other_id_no_i_c",
    },
    {
        "id": "d4279a74-377f-4f74-baf2-e1ebd001ec5c",
        "type": TYPE_IMAGE,
        "name": "other_id_photo",
        "lookup": "other_id_photo",
        "required": False,
        "label": {"English(EN)": "ID photo"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "other_id_type_i_c",
    },
    {
        "id": "b886d636-36cd-4beb-b2f9-6ddb204532d5",
        "type": TYPE_INTEGER,
        "name": "pregnant_member",
        "lookup": "pregnant_member",
        "required": True,
        "label": {
            "English(EN)": "How many pregnant women are there in the Household?"
        },
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "pregnant_member_h_c",
    },
    {
        "id": "07f7005f-e70d-409b-9dee-4c3414aba40b",
        "type": TYPE_INTEGER,
        "name": "female_age_group_0_5_count",
        "lookup": "female_age_group_0_5_count",
        "required": True,
        "label": {"English(EN)": "Females Age 0-5"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_0_5_age_group_h_c",
    },
    {
        "id": "6b993af8-4a5d-4a08-a444-8ade115c39ad",
        "type": TYPE_INTEGER,
        "name": "female_age_group_6_11_count",
        "lookup": "female_age_group_6_11_count",
        "required": True,
        "label": {"English(EN)": "Females Age 6-11"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_6_11_age_group_h_c",
    },
    {
        "id": "71ce16b5-4e49-48fa-818c-0bd2eba079eb",
        "type": TYPE_INTEGER,
        "name": "female_age_group_12_17_count",
        "lookup": "female_age_group_12_17_count",
        "required": True,
        "label": {"English(EN)": "Females Age 12-17"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_12_17_age_group_h_c",
    },
    {
        "id": "c157ad2d-dfee-4c03-8a8d-b550779696ff",
        "type": TYPE_INTEGER,
        "name": "female_adults_count",
        "lookup": "female_adults_count",
        "required": True,
        "label": {"English(EN)": "Female Adults"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_adults_h_c",
    },
    {
        "id": "18fd9429-400f-4fce-b72f-035d2afca201",
        "type": TYPE_INTEGER,
        "name": "pregnant_count",
        "lookup": "pregnant_count",
        "required": True,
        "label": {"English(EN)": "Pregnant females"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_pregnant_h_c",
    },
    {
        "id": "57233f1b-93c3-4fd4-a885-92c512c5e32a",
        "type": TYPE_INTEGER,
        "name": "male_age_group_0_5_count",
        "lookup": "male_age_group_0_5_count",
        "required": True,
        "label": {"English(EN)": "Males Age 0-5"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_0_5_age_group_h_c",
    },
    {
        "id": "11e2a938-e93a-4c18-8eca-7e61355d7476",
        "type": TYPE_INTEGER,
        "name": "male_age_group_6_11_count",
        "lookup": "male_age_group_6_11_count",
        "required": True,
        "label": {"English(EN)": "Males Age 6-11"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_6_11_age_group_h_c",
    },
    {
        "id": "bf28628e-0f6a-46e8-9587-3b0c17977006",
        "type": TYPE_INTEGER,
        "name": "male_age_group_12_17_count",
        "lookup": "male_age_group_12_17_count",
        "required": True,
        "label": {"English(EN)": "Males Age 12-17"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_12_17_age_group_h_c",
    },
    {
        "id": "48d464f5-3a45-4f8d-bfbb-a71cc16c0434",
        "type": TYPE_INTEGER,
        "name": "male_adults_count",
        "lookup": "male_adults_count",
        "required": True,
        "label": {"English(EN)": "Male Adults"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_adults_h_c",
    },
    {
        "id": "4f59aca6-5900-40c0-a1e4-47c331a90a6f",
        "type": TYPE_INTEGER,
        "name": "female_age_group_0_5_disabled_count",
        "lookup": "female_age_group_0_5_disabled_count",
        "required": True,
        "label": {"English(EN)": "Female members with Disability age 0-5"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_0_5_disability_h_c",
    },
    {
        "id": "10e33d7b-b3c4-4383-a4f0-6eba00a15e9c",
        "type": TYPE_INTEGER,
        "name": "female_age_group_6_11_disabled_count",
        "lookup": "female_age_group_6_11_disabled_count",
        "required": True,
        "label": {"English(EN)": "Female members with Disability age 6-11"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_6_11_disability_h_c",
    },
    {
        "id": "623a6fd6-d863-40cc-a4d1-964f739747be",
        "type": TYPE_INTEGER,
        "name": "female_age_group_12_17_disabled_count",
        "lookup": "female_age_group_12_17_disabled_count",
        "required": True,
        "label": {"English(EN)": "Female members with Disability age 12-17"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_12_17_disability_h_c",
    },
    {
        "id": "9eb7c4e5-f27f-4fe6-8956-ddbe712eb97b",
        "type": TYPE_INTEGER,
        "name": "female_adults_disabled_count",
        "lookup": "female_adults_disabled_count",
        "required": True,
        "label": {"English(EN)": "Female members with Disability adults"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "f_adults_disability_h_c",
    },
    {
        "id": "d3b82576-1bba-44fa-9d5a-db04e71bb35b",
        "type": TYPE_INTEGER,
        "name": "male_age_group_0_5_disabled_count",
        "lookup": "male_age_group_0_5_disabled_count",
        "required": True,
        "label": {"English(EN)": "Male members with Disability age 0-5"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_0_5_disability_h_c",
    },
    {
        "id": "78340f8f-86ab-464a-8e19-ce3d6feec5d6",
        "type": TYPE_INTEGER,
        "name": "male_age_group_6_11_disabled_count",
        "lookup": "male_age_group_6_11_disabled_count",
        "required": True,
        "label": {"English(EN)": "Male members with Disability age 6-11"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_6_11_disability_h_c",
    },
    {
        "id": "519140f7-1a9e-4115-b736-2b09dbc6f036",
        "type": TYPE_INTEGER,
        "name": "male_age_group_12_17_disabled_count",
        "lookup": "male_age_group_12_17_disabled_count",
        "required": True,
        "label": {"English(EN)": "Male members with Disability age 12-17"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_12_17_disability_h_c",
    },
    {
        "id": "3ca9b3de-12df-4bb3-9414-d26ae1fac9b8",
        "type": TYPE_INTEGER,
        "name": "male_adults_disabled_count",
        "lookup": "male_adults_disabled_count",
        "required": True,
        "label": {"English(EN)": "Male members with Disability adults"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "m_adults_disability_h_c",
    },
]

HOUSEHOLD_ID_FIELDS = [
    {
        "id": "746b3d2d-19c5-4b91-ad37-d230e1d33eb5",
        "type": TYPE_ID,
        "name": "household_id",
        "lookup": "household_id",
        "required": False,
        "label": {"English(EN)": "Household ID"},
        "hint": "",
        "choices": [],
        "associated_with": _HOUSEHOLD,
        "xlsx_field": "household_id",
    },
    {
        "id": "1079bfd0-fc51-41ab-aa10-667e6b2034b9",
        "type": TYPE_ID,
        "name": "household_id",
        "lookup": "household_id",
        "required": False,
        "label": {"English(EN)": "Household ID"},
        "hint": "",
        "choices": [],
        "associated_with": _INDIVIDUAL,
        "xlsx_field": "household_id",
    },
]


def _reduce_core_field_attr(old, new):
    old[new.get("name")] = new
    return old


def _core_fields_to_separated_dict(append_household_id=True):
    result_dict = {
        "individuals": {},
        "households": {},
    }

    core_fields_attrs = CORE_FIELDS_ATTRIBUTES

    if append_household_id:
        core_fields_attrs = HOUSEHOLD_ID_FIELDS + CORE_FIELDS_ATTRIBUTES

    for field in core_fields_attrs:
        associated_key = field["associated_with"].lower() + "s"
        result_dict[associated_key][field["xlsx_field"]] = field

    return result_dict


FILTERABLE_CORE_FIELDS_ATTRIBUTES = [
    x for x in CORE_FIELDS_ATTRIBUTES if x.get("type") in FILTERABLE_TYPES
]

CORE_FIELDS_ATTRIBUTES_DICTIONARY = reduce(
    _reduce_core_field_attr, CORE_FIELDS_ATTRIBUTES, {}
)

CORE_FIELDS_SEPARATED_WITH_NAME_AS_KEY = _core_fields_to_separated_dict()
