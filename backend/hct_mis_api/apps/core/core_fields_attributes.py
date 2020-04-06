import operator
from functools import reduce

from core.models import FlexibleAttribute
from core.utils import age_to_dob_query
from household.models import Household

TYPE_INTEGER = "INTEGER"
TYPE_SELECT_ONE = "SELECT_ONE"
_INDIVIDUAL = "Individual"
_HOUSEHOLD = "Household"
CORE_FIELDS_ATTRIBUTES = [
    {
        "id": "05c6be72-22ac-401b-9d3f-0a7e7352aa87",
        "type": TYPE_INTEGER,
        "name": "years_in_school",
        "label": {"English(EN)": "years in school"},
        "hint": "number of years spent in school",
        "required": True,
        "lookup": "individuals__years_in_school",
        "choices": [],
        "associated_with": _INDIVIDUAL,
    },
    {
        "id": "a1741e3c-0e24-4a60-8d2f-463943abaebb",
        "type": TYPE_INTEGER,
        "name": "age",
        "label": {"English(EN)": "age"},
        "hint": "age in years",
        "required": True,
        "get_query": age_to_dob_query,
        "choices": [],
        "associated_with": _INDIVIDUAL,
    },
    {
        "id": "d6aa9669-ae82-4e3c-adfe-79b5d95d0754",
        "type": TYPE_INTEGER,
        "lookup": "family_size",
        "name": "family_size",
        "label": {"English(EN)": "Family Size"},
        "hint": "how many persons in the household",
        "required": True,
        "choices": [],
        "associated_with": _HOUSEHOLD,
    },
    {
        "id": "3c2473d6-1e81-4025-86c7-e8036dd92f4b",
        "type": TYPE_SELECT_ONE,
        "name": "residence_status",
        "lookup": "residence_status",
        "required": True,
        "label": {"English(EN)": "Residence Status"},
        "hint": "residential status of household",
        "choices": [
            {"label": {"English(EN)": label}, "value": str(value),}
            for value, label in Household.RESIDENCE_STATUS_CHOICE
        ],
        "associated_with": _HOUSEHOLD,
    },
]


def _reduce_core_field_attr(old, new):
    old[new.get("name")] = new
    return old


CORE_FIELDS_ATTRIBUTES_DICTIONARY = reduce(
    _reduce_core_field_attr, CORE_FIELDS_ATTRIBUTES, {}
)
