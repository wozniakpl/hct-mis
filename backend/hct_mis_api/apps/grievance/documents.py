import logging

from django.conf import settings

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from hct_mis_api.apps.account.models import User
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.geo.models import Area
from hct_mis_api.apps.household.models import Household, Individual
from hct_mis_api.apps.registration_data.models import RegistrationDataImport

from .models import GrievanceTicket

logger = logging.getLogger(__name__)

INDEX = f"{settings.ELASTICSEARCH_INDEX_PREFIX}grievance_tickets"


def bulk_update_assigned_to(grievance_tickets_ids, assigned_to_id) -> None:
    es = Elasticsearch(settings.ELASTICSEARCH_HOST)

    documents_to_update = []
    for ticket_id in grievance_tickets_ids:
        document = {
            "_op_type": "update",
            "_index": INDEX,
            "_id": ticket_id,
            "_source": {"doc": {"assigned_to": {"id": str(assigned_to_id)}}},
        }
        documents_to_update.append(document)
        bulk(es, documents_to_update)
    logger.info(f"GrievanceDocuments with {','.join([str(_id) for _id in grievance_tickets_ids])} have been updated.")


@registry.register_document
class GrievanceTicketDocument(Document):
    unicef_id = fields.KeywordField()
    household_unicef_id = fields.KeywordField()
    registration_data_import = fields.ObjectField(properties={"id": fields.KeywordField()})
    admin2 = fields.ObjectField(properties={"id": fields.KeywordField()})
    business_area = fields.ObjectField(properties={"slug": fields.KeywordField()})
    category = fields.KeywordField(attr="category")
    status = fields.KeywordField(attr="status")
    issue_type = fields.KeywordField(attr="issue_type")
    priority = fields.KeywordField(attr="priority")
    urgency = fields.KeywordField(attr="urgency")
    grievance_type = fields.KeywordField(attr="grievance_type_to_string")
    assigned_to = fields.ObjectField(properties={"id": fields.KeywordField()})
    ticket_details = fields.ObjectField(
        properties={
            "household": fields.ObjectField(
                properties={"head_of_household": fields.ObjectField(properties={"family_name": fields.KeywordField()})}
            )
        }
    )

    class Django:
        model = GrievanceTicket
        fields = [
            "created_at",
        ]
        related_models = [Area, BusinessArea, Household, Individual, RegistrationDataImport, User]

    class Index:
        name = INDEX
        settings = settings.ELASTICSEARCH_BASE_SETTINGS

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, BusinessArea):
            return related_instance.tickets.all()
