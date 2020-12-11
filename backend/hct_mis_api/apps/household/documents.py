from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core.es_analyzers import phonetic_analyzer
from .models import Individual


@registry.register_document
class IndividualDocument(Document):
    id = fields.KeywordField(boost=0)
    given_name = fields.TextField(analyzer=phonetic_analyzer)
    middle_name = fields.TextField(analyzer=phonetic_analyzer)
    family_name = fields.TextField(analyzer=phonetic_analyzer)
    full_name = fields.TextField(analyzer=phonetic_analyzer)
    birth_date = fields.DateField()
    phone_no = fields.KeywordField("phone_no.__str__")
    phone_no_alternative = fields.KeywordField("phone_no_alternative.__str__")
    business_area = fields.KeywordField()
    admin1 = fields.KeywordField()
    admin2 = fields.KeywordField()
    household = fields.ObjectField(
        properties={
            "residence_status": fields.KeywordField(),
            "country_origin": fields.KeywordField(attr="country_origin.alpha3"),
            "size": fields.IntegerField(),
            "address": fields.TextField(),
            "country": fields.KeywordField(attr="country.alpha3"),
            "female_age_group_0_5_count": fields.IntegerField(),
            "female_age_group_6_11_count": fields.IntegerField(),
            "female_age_group_12_17_count": fields.IntegerField(),
            "female_adults_count": fields.IntegerField(),
            "pregnant_count": fields.IntegerField(),
            "male_age_group_0_5_count": fields.IntegerField(),
            "male_age_group_6_11_count": fields.IntegerField(),
            "male_age_group_12_17_count": fields.IntegerField(),
            "male_adults_count": fields.IntegerField(),
            "female_age_group_0_5_disabled_count": fields.IntegerField(),
            "female_age_group_6_11_disabled_count": fields.IntegerField(),
            "female_age_group_12_17_disabled_count": fields.IntegerField(),
            "female_adults_disabled_count": fields.IntegerField(),
            "male_age_group_0_5_disabled_count": fields.IntegerField(),
            "male_age_group_6_11_disabled_count": fields.IntegerField(),
            "male_age_group_12_17_disabled_count": fields.IntegerField(),
            "male_adults_disabled_count": fields.IntegerField(),
            "head_of_household": fields.KeywordField(attr="head_of_household.id"),
            "returnee": fields.BooleanField(),
        }
    )
    documents = fields.ObjectField(
        properties={
            "number": fields.KeywordField(attr="document_number"),
            "type": fields.KeywordField(attr="type.type"),
        }
    )
    identities = fields.ObjectField(
        properties={"number": fields.KeywordField(), "agency": fields.KeywordField(attr="agency.type")}
    )
    households_and_roles = fields.ObjectField(
        properties={"role": fields.KeywordField(), "individual": fields.KeywordField(attr="individual.id")}
    )

    def prepare_admin1(self, instance):
        household = instance.household
        if household:
            admin_area = household.admin_area
            if admin_area:
                return admin_area.title
            return

    def prepare_admin2(self, instance):
        household = instance.household
        if household:
            admin_area = household.admin_area
            if admin_area:
                children = admin_area.children.filter(admin_area_type__admin_level=2).first()
                if children:
                    return children.title
                return

    def prepare_hash_key(self, instance):
        return instance.get_hash_key

    def prepare_business_area(self, instance):
        return instance.registration_data_import.business_area.slug

    class Index:
        name = "individuals"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Individual

        fields = [
            "relationship",
            "sex",
            "created_at",
            "updated_at",
        ]
