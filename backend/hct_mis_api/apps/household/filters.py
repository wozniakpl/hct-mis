import logging
from typing import TYPE_CHECKING, Any, Dict, List

from django.db.models import Q, QuerySet
from django.db.models.functions import Lower

from constance import config
from django_filters import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    OrderingFilter,
)

from hct_mis_api.apps.core.exceptions import SearchException
from hct_mis_api.apps.core.filters import (
    AgeRangeFilter,
    BusinessAreaSlugFilter,
    DateRangeFilter,
    IntegerRangeFilter,
)
from hct_mis_api.apps.core.utils import (
    CustomOrderingFilter,
    decode_id_string,
    decode_id_string_required,
)
from hct_mis_api.apps.geo.models import Area
from hct_mis_api.apps.household.documents import HouseholdDocument, get_individual_doc
from hct_mis_api.apps.household.models import (
    DUPLICATE,
    DUPLICATE_IN_BATCH,
    INDIVIDUAL_FLAGS_CHOICES,
    INDIVIDUAL_STATUS_CHOICES,
    NEEDS_ADJUDICATION,
    SANCTION_LIST_CONFIRMED_MATCH,
    SANCTION_LIST_POSSIBLE_MATCH,
    SEX_CHOICE,
    STATUS_ACTIVE,
    STATUS_DUPLICATE,
    STATUS_WITHDRAWN,
    DocumentType,
    Household,
    Individual,
)
from hct_mis_api.apps.program.models import Program

if TYPE_CHECKING:
    from hct_mis_api.apps.core.models import BusinessArea

logger = logging.getLogger(__name__)


def _prepare_kobo_asset_id_value(code: str) -> str:
    """
    preparing value for filter by kobo_asset_id
    value examples KOBO-111222, HOPE-20220531-3/111222, HOPE-2022530111222
    return asset_id number like 111222
    """
    if len(code) < 6:
        return code

    code = code[5:].split("/")[-1]  # remove prefix 'KOBO-' and split ['20220531-3', '111222']
    if code.startswith("20223"):
        # month 3 day 25...31 id is 44...12067
        code = code[7:]

    if code.startswith("20224"):
        # TODO: not sure if this one is correct?
        # code[5] is the day of month (or the first digit of it)
        # month 4 id is 12068..157380
        if len(code) == 12 and code[5] in ["1", "2", "3"]:
            code = code[-5:]
        else:
            code = code[-6:]

    if code.startswith("20225"):
        # month 5 id is 157381...392136
        code = code[-6:]

    if code.startswith("20226"):
        # month 6 id is 392137...
        code = code[-6:]
    return code


class HouseholdFilter(FilterSet):
    business_area = BusinessAreaSlugFilter()
    size = IntegerRangeFilter(field_name="size")
    search = CharFilter(method="search_filter")
    search_type = CharFilter(method="search_type_filter")
    head_of_household__full_name = CharFilter(field_name="head_of_household__full_name", lookup_expr="startswith")
    head_of_household__phone_no_valid = BooleanFilter(method="phone_no_valid_filter")
    last_registration_date = DateRangeFilter(field_name="last_registration_date")
    withdrawn = BooleanFilter(field_name="withdrawn")
    country_origin = CharFilter(field_name="country_origin__iso_code3", lookup_expr="startswith")
    program = CharFilter(method="filter_by_program")
    is_active_program = BooleanFilter(method="filter_is_active_program")

    class Meta:
        model = Household
        fields = {
            "business_area": ["exact"],
            "address": ["exact", "startswith"],
            "head_of_household__full_name": ["exact", "startswith"],
            "size": ["range", "lte", "gte"],
            "admin_area": ["exact"],
            "admin2": ["exact"],
            "target_populations": ["exact"],
            "residence_status": ["exact"],
            "withdrawn": ["exact"],
        }

    order_by = CustomOrderingFilter(
        fields=(
            "age",
            "sex",
            "household__id",
            "id",
            "unicef_id",
            "household_ca_id",
            "size",
            "status_label",
            Lower("head_of_household__full_name"),
            Lower("admin_area__name"),
            "residence_status",
            Lower("registration_data_import__name"),
            "total_cash_received",
            "last_registration_date",
            "first_registration_date",
        )
    )

    def phone_no_valid_filter(self, qs: QuerySet, name: str, value: bool) -> QuerySet:
        """
        Filter households by phone_no_valid
        True: get households with valid phone_no or valid phone_no_alternative
        False: get households with invalid both phone_no and invalid phone_no_alternative
        """
        if value is True:
            return qs.exclude(
                head_of_household__phone_no_valid=False, head_of_household__phone_no_alternative_valid=False
            )
        elif value is False:
            return qs.filter(
                head_of_household__phone_no_valid=False, head_of_household__phone_no_alternative_valid=False
            )
        return qs

    def _search_es(self, qs: QuerySet, value: Any) -> QuerySet:
        business_area = self.data["business_area"]
        search = value.strip()
        search_type = self.data.get("search_type")

        if search_type == "kobo_asset_id":
            split_values_list = search.split(" ")
            inner_query = Q()
            for split_value in split_values_list:
                striped_value = split_value.strip(",")
                if striped_value.startswith(("HOPE-", "KOBO-")):
                    _value = _prepare_kobo_asset_id_value(search)
                    # if user put somethink like 'KOBO-111222', 'HOPE-20220531-3/111222', 'HOPE-2022531111222'
                    # will filter by '111222' like 111222 is ID
                    inner_query |= Q(kobo_asset_id__endswith=_value)
            return qs.filter(inner_query).distinct()

        query_dict = get_elasticsearch_query_for_households(search, search_type, business_area)
        es_response = (
            HouseholdDocument.search().params(search_type="dfs_query_then_fetch").update_from_dict(query_dict).execute()
        )
        es_ids = [x.meta["id"] for x in es_response]
        return qs.filter(id__in=es_ids)

    def search_filter(self, qs: QuerySet[Household], name: str, value: Any) -> QuerySet[Household]:
        try:
            if config.USE_ELASTICSEARCH_FOR_HOUSEHOLDS_SEARCH:
                return self._search_es(qs, value)
            return self._search_db(qs, value)
        except SearchException:
            return qs.none()

    def _search_db(self, qs: QuerySet[Household], value: str) -> QuerySet[Household]:
        search = value.strip()
        search_type = self.data.get("search_type")

        if search_type == "household_id":
            return qs.filter(unicef_id__icontains=search)
        if search_type == "individual_id":
            return qs.filter(head_of_household__unicef_id__icontains=search)
        if search_type == "full_name":
            return qs.filter(head_of_household__full_name__icontains=search)
        if search_type == "phone_no":
            return qs.filter(
                Q(head_of_household__phone_no__icontains=search)
                | Q(head_of_household__phone_no_alternative__icontains=search)
            )
        if search_type == "registration_id":
            try:
                int(search)
            except ValueError:
                raise SearchException("The search value for a given search type should be a number")
            return qs.filter(registration_id__icontains=search)
        if search_type == "kobo_asset_id":
            inner_query = Q()
            split_values_list = search.split(" ")
            for split_value in split_values_list:
                striped_value = split_value.strip(",")
                if striped_value.startswith(("HOPE-", "KOBO-")):
                    _value = _prepare_kobo_asset_id_value(search)
                    # if user put something like 'KOBO-111222', 'HOPE-20220531-3/111222', 'HOPE-2022531111222'
                    # will filter by '111222' like 111222 is ID
                    inner_query |= Q(kobo_asset_id__endswith=_value)
                else:
                    inner_query = Q(kobo_asset_id__endswith=search)
            return qs.filter(inner_query)
        if search_type == "bank_account_number":
            return qs.filter(head_of_household__bank_account_info__bank_account_number__icontains=search)
        if DocumentType.objects.filter(key=search_type).exists():
            return qs.filter(
                head_of_household__documents__type__key=search_type,
                head_of_household__documents__document_number__icontains=search,
            )
        raise SearchException(f"Invalid search key '{search_type}'")

    def search_type_filter(self, qs: QuerySet[Household], name: str, value: str) -> QuerySet[Household]:
        return qs

    def filter_is_active_program(self, qs: QuerySet, name: str, value: bool) -> QuerySet:
        # TODO: after data migrations will use only program
        if value is True:
            return qs.filter(Q(programs__status=Program.ACTIVE) | Q(program__status=Program.ACTIVE))
        elif value is False:
            return qs.filter(Q(programs__status=Program.FINISHED) | Q(program__status=Program.FINISHED))
        else:
            return qs

    def filter_by_program(self, qs: "QuerySet", name: str, value: str) -> "QuerySet[Household]":
        # TODO: after data migrations will use only program
        return qs.filter(
            Q(programs__id=decode_id_string_required(value)) | Q(program__id=decode_id_string_required(value))
        ).distinct()


class IndividualFilter(FilterSet):
    business_area = BusinessAreaSlugFilter()
    age = AgeRangeFilter(field_name="birth_date")
    sex = MultipleChoiceFilter(field_name="sex", choices=SEX_CHOICE)
    programs = ModelMultipleChoiceFilter(field_name="household__programs", queryset=Program.objects.all())
    search = CharFilter(method="search_filter")
    search_type = CharFilter(method="search_type_filter")
    last_registration_date = DateRangeFilter(field_name="last_registration_date")
    admin2 = ModelMultipleChoiceFilter(
        field_name="household__admin_area", queryset=Area.objects.filter(area_type__area_level=2)
    )
    status = MultipleChoiceFilter(choices=INDIVIDUAL_STATUS_CHOICES, method="status_filter")
    excluded_id = CharFilter(method="filter_excluded_id")
    withdrawn = BooleanFilter(field_name="withdrawn")
    flags = MultipleChoiceFilter(choices=INDIVIDUAL_FLAGS_CHOICES, method="flags_filter")
    program = CharFilter(method="filter_by_program")
    is_active_program = BooleanFilter(method="filter_is_active_program")

    class Meta:
        model = Individual
        fields = {
            "household__id": ["exact"],
            "business_area": ["exact"],
            "full_name": ["exact", "startswith", "endswith"],
            "sex": ["exact"],
            "household__admin_area": ["exact"],
            "withdrawn": ["exact"],
        }

    order_by = CustomOrderingFilter(
        fields=(
            "id",
            "unicef_id",
            Lower("full_name"),
            "household__id",
            "household__unicef_id",
            "birth_date",
            "sex",
            "relationship",
            Lower("household__admin_area__name"),
            "last_registration_date",
            "first_registration_date",
        )
    )

    def flags_filter(self, qs: QuerySet, name: str, value: List[str]) -> QuerySet:
        q_obj = Q()
        if NEEDS_ADJUDICATION in value:
            q_obj |= Q(deduplication_golden_record_status=NEEDS_ADJUDICATION)
        if DUPLICATE in value:
            q_obj |= Q(duplicate=True)
        if SANCTION_LIST_POSSIBLE_MATCH in value:
            q_obj |= Q(sanction_list_possible_match=True, sanction_list_confirmed_match=False)
        if SANCTION_LIST_CONFIRMED_MATCH in value:
            q_obj |= Q(sanction_list_confirmed_match=True)

        return qs.filter(q_obj)

    def _search_es(self, qs: QuerySet[Individual], value: str) -> QuerySet[Individual]:
        business_area = self.data["business_area"]
        search_type = self.data.get("search_type")
        search = value.strip()
        query_dict = get_elasticsearch_query_for_individuals(search, search_type, business_area)
        es_response = (
            get_individual_doc(business_area)
            .search()
            .params(search_type="dfs_query_then_fetch")
            .update_from_dict(query_dict)
            .execute()
        )

        es_ids = [x.meta["id"] for x in es_response]
        return qs.filter(Q(id__in=es_ids)).distinct()

    def search_filter(self, qs: QuerySet[Individual], name: str, value: Any) -> QuerySet[Individual]:
        try:
            if config.USE_ELASTICSEARCH_FOR_INDIVIDUALS_SEARCH:
                return self._search_es(qs, value)
            return self._search_db(qs, value)
        except SearchException:
            return qs.none()

    def _search_db(self, qs: QuerySet[Individual], value: str) -> QuerySet[Individual]:
        search_type = self.data.get("search_type")
        search = value.strip()
        if search_type == "individual_id":
            return qs.filter(unicef_id__icontains=search)
        if search_type == "household_id":
            return qs.filter(household__unicef_id__icontains=search)
        if search_type == "full_name":
            return qs.filter(full_name__icontains=search)
        if search_type == "phone_no":
            return qs.filter(Q(phone_no__icontains=search) | Q(phone_no_alternative__icontains=search))
        if search_type == "registration_id":
            try:
                int(search)
            except ValueError:
                raise SearchException("The search value for a given search type should be a number")
            return qs.filter(registration_id__icontains=search)
        if search_type == "bank_account_number":
            return qs.filter(bank_account_info__bank_account_number__icontains=search)
        if DocumentType.objects.filter(key=search_type).exists():
            return qs.filter(documents__type__key=search_type, documents__document_number__icontains=search)
        raise SearchException(f"Invalid search key '{search_type}'")

    def search_type_filter(self, qs: QuerySet[Individual], name: str, value: str) -> QuerySet[Individual]:
        return qs

    def status_filter(self, qs: QuerySet, name: str, value: List[str]) -> QuerySet:
        q_obj = Q()
        if STATUS_DUPLICATE in value:
            q_obj |= Q(duplicate=True)
        if STATUS_WITHDRAWN in value:
            q_obj |= Q(withdrawn=True)
        if STATUS_ACTIVE in value:
            q_obj |= Q(duplicate=False, withdrawn=False)

        return qs.filter(q_obj).distinct()

    def filter_excluded_id(self, qs: QuerySet, name: str, value: Any) -> QuerySet:
        return qs.exclude(id=decode_id_string(value))

    def filter_is_active_program(self, qs: QuerySet, name: str, value: bool) -> "QuerySet[Individual]":
        # TODO: after data migrations will use only program
        if value is True:
            return qs.filter(
                Q(household__programs__status=Program.ACTIVE) | Q(household__program__status=Program.ACTIVE)
            )
        elif value is False:
            return qs.filter(
                Q(household__programs__status=Program.FINISHED) | Q(household__program__status=Program.FINISHED)
            )
        else:
            return qs

    def filter_by_program(self, qs: "QuerySet", name: str, value: str) -> "QuerySet[Individual]":
        # TODO: after data migrations will use only program
        return qs.filter(
            Q(household__programs__id=decode_id_string_required(value))
            | Q(household__program__id=decode_id_string_required(value))
        ).distinct()


def get_elasticsearch_query_for_individuals(search: str, search_type: str, business_area: "BusinessArea") -> Dict:
    all_queries: List = []

    if search_type == "individual_id":
        all_queries.append({"match_phrase_prefix": {"unicef_id": {"query": search}}})
    elif search_type == "household_id":
        all_queries.append({"match_phrase_prefix": {"household.unicef_id": {"query": search}}})
    elif search_type == "full_name":
        all_queries.append({"match_phrase_prefix": {"full_name": {"query": search}}})
    elif search_type == "phone_no":
        all_queries.append({"match_phrase_prefix": {"phone_no_text": {"query": search}}})
        all_queries.append(
            {"match_phrase_prefix": {"phone_no_alternative_text": {"query": search}}},
        )
    elif search_type == "registration_id":
        try:
            int(search)
        except ValueError:
            raise SearchException("The search value for a given search type should be a number")
        all_queries.append({"match_phrase_prefix": {"registration_id": {"query": search}}})
    elif search_type == "bank_account_number":
        all_queries.append({"match_phrase_prefix": {"bank_account_info.bank_account_number": {"query": search}}})
    elif DocumentType.objects.filter(key=search_type).exists():
        all_queries.append(
            {
                "bool": {
                    "must": [
                        {"match": {"documents.number": {"query": search}}},
                        {"match": {"documents.key": {"query": search_type}}},
                    ],
                },
            }
        )
    else:
        raise SearchException(f"Invalid search key '{search_type}'")

    return {
        "size": "100",
        "_source": False,
        "query": {
            "bool": {
                "filter": {"term": {"business_area": business_area}},
                "minimum_should_match": 1,
                "should": all_queries,
            }
        },
    }


def get_elasticsearch_query_for_households(search: str, search_type: str, business_area: "BusinessArea") -> Dict:
    all_queries: List = []

    if search_type == "household_id":
        all_queries.append({"match_phrase_prefix": {"unicef_id": {"query": search}}})
    elif search_type == "individual_id":
        all_queries.append({"match_phrase_prefix": {"head_of_household.unicef_id": {"query": search}}})
    elif search_type == "full_name":
        all_queries.append({"match_phrase_prefix": {"head_of_household.full_name": {"query": search}}})
    elif search_type == "phone_no":
        all_queries.append({"match_phrase_prefix": {"head_of_household.phone_no_text": {"query": search}}})
        all_queries.append({"match_phrase_prefix": {"head_of_household.phone_no_alternative_text": {"query": search}}})
    elif search_type == "bank_account_number":
        all_queries.append(
            {"match_phrase_prefix": {"head_of_household.bank_account_info.bank_account_number": {"query": search}}}
        )
    elif search_type == "registration_id":
        try:
            int(search)
        except ValueError:
            raise SearchException("The search value for a given search type should be a number")
        all_queries.append({"match_phrase_prefix": {"registration_id": {"query": search}}})
    elif search_type == "kobo_asset_id":
        # Handled on postgres side
        pass
    elif DocumentType.objects.filter(key=search_type).exists():
        all_queries.append(
            {
                "bool": {
                    "must": [
                        {"match": {"head_of_household.documents.number": {"query": search}}},
                        {"match": {"head_of_household.documents.key": {"query": search_type}}},
                    ],
                },
            }
        )
    else:
        raise SearchException(f"Invalid search key '{search_type}'")

    query: Dict[str, Any] = {
        "size": "100",
        "_source": False,
        "query": {
            "bool": {
                "minimum_should_match": 1,
                "should": all_queries,
            }
        },
    }
    if config.USE_ELASTICSEARCH_FOR_HOUSEHOLDS_SEARCH_USE_BUSINESS_AREA:
        query["query"]["bool"]["filter"] = ({"term": {"business_area": business_area}},)
    return query


class MergedHouseholdFilter(FilterSet):
    """
    This filter emulates ImportedHousehold filter for data structure which is linked to Import Preview when RDI is merged
    """

    business_area = CharFilter(field_name="business_area__slug")
    rdi_id = CharFilter(method="filter_rdi_id")

    class Meta:
        model = Household
        fields = ()

    order_by = CustomOrderingFilter(
        fields=(
            "id",
            Lower("head_of_household__full_name"),
            "size",
            "first_registration_date",
            "admin2_title",
        )
    )

    def filter_rdi_id(self, queryset: "QuerySet", model_field: Any, value: str) -> "QuerySet":
        return queryset.filter(registration_data_import_id=decode_id_string(value))


class MergedIndividualFilter(FilterSet):
    """
    This filter emulates ImportedIndividual filter for data structure which is linked to Import Preview when RDI is merged
    """

    rdi_id = CharFilter(method="filter_rdi_id")
    duplicates_only = BooleanFilter(method="filter_duplicates_only")
    business_area = CharFilter(field_name="business_area__slug")

    class Meta:
        model = Individual
        fields = ("household",)

    order_by = OrderingFilter(
        fields=(
            "unicef_id",
            "id",
            "full_name",
            "birth_date",
            "sex",
            "deduplication_batch_status",
            "deduplication_golden_record_status",
        )
    )

    def filter_rdi_id(self, queryset: "QuerySet", model_field: Any, value: str) -> "QuerySet":
        return queryset.filter(registration_data_import_id=decode_id_string(value))

    def filter_duplicates_only(self, queryset: "QuerySet", model_field: Any, value: bool) -> "QuerySet":
        if value:
            return queryset.filter(
                Q(deduplication_golden_record_status=DUPLICATE) | Q(deduplication_batch_status=DUPLICATE_IN_BATCH)
            )
        return queryset
