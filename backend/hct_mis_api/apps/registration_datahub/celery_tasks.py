import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from django.core.cache import cache
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from sentry_sdk import configure_scope

from hct_mis_api.apps.core.celery import app
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.models import Document
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.registration_datahub.models import ImportedHousehold
from hct_mis_api.apps.registration_datahub.tasks.deduplicate import (
    HardDocumentDeduplication,
)
from hct_mis_api.apps.utils.logs import log_start_and_end
from hct_mis_api.apps.utils.sentry import sentry_tags

if TYPE_CHECKING:
    from uuid import UUID

    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


def handle_rdi_exception(datahub_rdi_id: str, e: BaseException) -> None:
    try:
        from sentry_sdk import capture_exception

        err = capture_exception(e)
    except Exception:
        err = "N/A"

    RegistrationDataImport.objects.filter(
        datahub_id=datahub_rdi_id,
    ).update(status=RegistrationDataImport.IMPORT_ERROR, sentry_id=err, error_message=str(e))


@contextmanager
def locked_cache(key: Union[int, str], timeout: int = 60 * 60 * 24) -> Any:
    now = timezone.now()
    try:
        if cache.get_or_set(key, now, timeout=timeout) == now:
            logger.info(f"Task with key {key} started")
            yield True
        else:
            logger.info(f"Task with key {key} is already running")
            yield False
    finally:
        cache.delete(key)
        logger.info(f"Task with key {key} finished")


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def registration_xlsx_import_task(
    self: Any, registration_data_import_id: str, import_data_id: str, business_area_id: str, program_id: "UUID"
) -> None:
    try:
        from hct_mis_api.apps.core.models import BusinessArea
        from hct_mis_api.apps.registration_datahub.tasks.rdi_xlsx_create import (
            RdiXlsxCreateTask,
        )

        with locked_cache(key=f"registration_xlsx_import_task-{registration_data_import_id}") as locked:
            if not locked:
                raise Exception(
                    f"Task with key registration_xlsx_import_task {registration_data_import_id} is already running"
                )
            with configure_scope() as scope:
                scope.set_tag("business_area", BusinessArea.objects.get(pk=business_area_id))
                rdi = RegistrationDataImport.objects.get(datahub_id=registration_data_import_id)
                if rdi.status != RegistrationDataImport.IMPORT_SCHEDULED:
                    raise Exception("Rdi is not in status IMPORT_SCHEDULED while trying to import")
                rdi.status = RegistrationDataImport.IMPORTING
                rdi.save()
                RdiXlsxCreateTask().execute(
                    registration_data_import_id=registration_data_import_id,
                    import_data_id=import_data_id,
                    business_area_id=business_area_id,
                    program_id=str(program_id),
                )
    except Exception as e:
        logger.warning(e)
        from hct_mis_api.apps.registration_datahub.models import (
            RegistrationDataImportDatahub,
        )

        RegistrationDataImportDatahub.objects.filter(
            id=registration_data_import_id,
        ).update(import_done=RegistrationDataImportDatahub.DONE)

        handle_rdi_exception(registration_data_import_id, e)
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def registration_kobo_import_task(
    self: Any, registration_data_import_id: str, import_data_id: str, business_area_id: str, program_id: "UUID"
) -> None:
    try:
        from hct_mis_api.apps.core.models import BusinessArea
        from hct_mis_api.apps.registration_datahub.tasks.rdi_kobo_create import (
            RdiKoboCreateTask,
        )

        with configure_scope() as scope:
            scope.set_tag("business_area", BusinessArea.objects.get(pk=business_area_id))

            RdiKoboCreateTask().execute(
                registration_data_import_id=registration_data_import_id,
                import_data_id=import_data_id,
                business_area_id=business_area_id,
                program_id=str(program_id),
            )
    except Exception as e:
        logger.warning(e)
        from hct_mis_api.apps.registration_datahub.models import (
            RegistrationDataImportDatahub,
        )

        RegistrationDataImportDatahub.objects.filter(
            id=registration_data_import_id,
        ).update(import_done=RegistrationDataImportDatahub.DONE)

        handle_rdi_exception(registration_data_import_id, e)
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def registration_kobo_import_hourly_task(self: Any) -> None:
    try:
        from hct_mis_api.apps.core.models import BusinessArea
        from hct_mis_api.apps.registration_datahub.models import (
            RegistrationDataImportDatahub,
        )
        from hct_mis_api.apps.registration_datahub.tasks.rdi_kobo_create import (
            RdiKoboCreateTask,
        )

        not_started_rdi = RegistrationDataImportDatahub.objects.filter(
            import_done=RegistrationDataImportDatahub.NOT_STARTED
        ).first()

        if not_started_rdi is None:
            return
        business_area = BusinessArea.objects.get(slug=not_started_rdi.business_area_slug)
        program_id = RegistrationDataImport.objects.get(id=not_started_rdi.hct_id).program.id
        with configure_scope() as scope:
            scope.set_tag("business_area", business_area)

            RdiKoboCreateTask().execute(
                registration_data_import_id=str(not_started_rdi.id),
                import_data_id=str(not_started_rdi.import_data.id),
                business_area_id=str(business_area.id),
                program_id=str(program_id),
            )
    except Exception as e:
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def registration_xlsx_import_hourly_task(self: Any) -> None:
    try:
        from hct_mis_api.apps.core.models import BusinessArea
        from hct_mis_api.apps.registration_datahub.models import (
            RegistrationDataImportDatahub,
        )
        from hct_mis_api.apps.registration_datahub.tasks.rdi_xlsx_create import (
            RdiXlsxCreateTask,
        )

        not_started_rdi = RegistrationDataImportDatahub.objects.filter(
            import_done=RegistrationDataImportDatahub.NOT_STARTED
        ).first()
        if not_started_rdi is None:
            return

        business_area = BusinessArea.objects.get(slug=not_started_rdi.business_area_slug)
        program_id = RegistrationDataImport.objects.get(id=not_started_rdi.hct_id).program.id
        with configure_scope() as scope:
            scope.set_tag("business_area", business_area)

            RdiXlsxCreateTask().execute(
                registration_data_import_id=str(not_started_rdi.id),
                import_data_id=str(not_started_rdi.import_data.id),
                business_area_id=str(business_area.id),
                program_id=str(program_id),
            )
    except Exception as e:
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def merge_registration_data_import_task(self: Any, registration_data_import_id: str) -> bool:
    logger.info(
        f"merge_registration_data_import_task started for registration_data_import_id: {registration_data_import_id}"
    )
    with locked_cache(key=f"merge_registration_data_import_task-{registration_data_import_id}") as locked:
        if not locked:
            return True
        try:
            from hct_mis_api.apps.registration_data.models import RegistrationDataImport
            from hct_mis_api.apps.registration_datahub.tasks.rdi_merge import (
                RdiMergeTask,
            )

            RegistrationDataImport.objects.filter(id=registration_data_import_id).update(
                status=RegistrationDataImport.MERGING
            )

            RdiMergeTask().execute(registration_data_import_id)
        except Exception as e:
            logger.exception(e)
            from hct_mis_api.apps.registration_data.models import RegistrationDataImport

            RegistrationDataImport.objects.filter(
                id=registration_data_import_id,
            ).update(status=RegistrationDataImport.MERGE_ERROR)
            raise self.retry(exc=e)

    logger.info(
        f"merge_registration_data_import_task finished for registration_data_import_id: {registration_data_import_id}"
    )
    return True


@app.task(bind=True, queue="priority", default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def rdi_deduplication_task(self: Any, registration_data_import_id: str) -> None:
    try:
        from hct_mis_api.apps.registration_datahub.models import (
            RegistrationDataImportDatahub,
        )
        from hct_mis_api.apps.registration_datahub.tasks.deduplicate import (
            DeduplicateTask,
        )

        rdi_obj = RegistrationDataImportDatahub.objects.get(id=registration_data_import_id)
        program_id = RegistrationDataImport.objects.get(id=rdi_obj.hct_id).program.id

        with configure_scope() as scope:
            scope.set_tag("business_area", rdi_obj.business_area_slug)

            with transaction.atomic(using="default"), transaction.atomic(using="registration_datahub"):
                DeduplicateTask(rdi_obj.business_area_slug, program_id).deduplicate_imported_individuals(
                    registration_data_import_datahub=rdi_obj
                )
    except Exception as e:
        handle_rdi_exception(registration_data_import_id, e)
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def pull_kobo_submissions_task(self: Any, import_data_id: "UUID") -> Dict:
    from hct_mis_api.apps.registration_datahub.models import KoboImportData

    kobo_import_data = KoboImportData.objects.get(id=import_data_id)
    from hct_mis_api.apps.registration_datahub.tasks.pull_kobo_submissions import (
        PullKoboSubmissions,
    )

    try:
        return PullKoboSubmissions().execute(kobo_import_data)
    except Exception as e:
        from hct_mis_api.apps.registration_data.models import RegistrationDataImport

        RegistrationDataImport.objects.filter(
            id=kobo_import_data.id,
        ).update(status=KoboImportData.STATUS_ERROR, error=str(e))
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def validate_xlsx_import_task(self: Any, import_data_id: "UUID") -> Dict:
    from hct_mis_api.apps.registration_datahub.models import ImportData

    import_data = ImportData.objects.get(id=import_data_id)
    from hct_mis_api.apps.registration_datahub.tasks.validatate_xlsx_import import (
        ValidateXlsxImport,
    )

    try:
        return ValidateXlsxImport().execute(import_data)
    except Exception as e:
        ImportData.objects.filter(
            id=import_data.id,
        ).update(status=ImportData.STATUS_ERROR, error=str(e))
        raise self.retry(exc=e)


def check_and_set_taxid(queryset: "QuerySet") -> Dict:
    qs = queryset.filter(unique_field__isnull=True)
    results = {"updated": [], "processed": [], "errors": []}
    for record in qs.all():
        try:
            for individual in record.fields["individuals"]:
                if individual["role_i_c"] == "y":
                    record.unique_field = individual["tax_id_no_i_c"]
                    record.save()
                    results["updated"].append(record.pk)
                    break
            results["processed"].append(record.pk)

        except Exception as e:
            results["errors"].append(f"Record: {record.pk} - {e.__class__.__name__}: {str(e)}")
    return results


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def automate_registration_diia_import_task(
    self: Any, program_id: "UUID", page_size: int, template: str = "Diia ukraine rdi {date} {page_size}", **filters: Any
) -> List:
    from hct_mis_api.apps.core.models import BusinessArea
    from hct_mis_api.apps.program.models import Program
    from hct_mis_api.apps.registration_datahub.tasks.rdi_diia_create import (
        RdiDiiaCreateTask,
    )

    with locked_cache(key="automate_rdi_diia_creation_task") as locked:
        if not locked:
            return []
        try:
            with configure_scope() as scope:
                scope.set_tag("business_area", BusinessArea.objects.get(slug="ukraine"))
                service = RdiDiiaCreateTask()
                rdi_name = template.format(
                    date=timezone.now(),
                    page_size=page_size,
                )
                program = Program.objects.get(id=program_id)
                rdi = service.create_rdi(imported_by=None, program=program, rdi_name=rdi_name)
                service.execute(rdi.id, diia_hh_count=page_size)
                return [rdi_name, page_size]
        except Exception as e:
            raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def registration_diia_import_task(
    self: Any,
    program_id: "UUID",
    diia_hh_ids: List,
    template: str = "Diia ukraine rdi {date} {page_size}",
    **filters: Any,
) -> List:
    from hct_mis_api.apps.core.models import BusinessArea
    from hct_mis_api.apps.program.models import Program
    from hct_mis_api.apps.registration_datahub.tasks.rdi_diia_create import (
        RdiDiiaCreateTask,
    )

    with locked_cache(key="registration_diia_import_task") as locked:
        if not locked:
            return []
        try:
            with configure_scope() as scope:
                scope.set_tag("business_area", BusinessArea.objects.get(slug="ukraine"))
                service = RdiDiiaCreateTask()
                rdi_name = template.format(
                    date=timezone.now(),
                    page_size=len(diia_hh_ids),
                )
                program = Program.objects.get(id=program_id)
                rdi = service.create_rdi(imported_by=None, program=program, rdi_name=rdi_name)
                service.execute(rdi.id, diia_hh_ids=diia_hh_ids)
                return [rdi_name, len(diia_hh_ids)]
        except Exception as e:
            raise self.retry(exc=e)


@app.task
@log_start_and_end
@sentry_tags
def deduplicate_documents() -> bool:
    with locked_cache(key="deduplicate_documents") as locked:
        if not locked:
            return True
        grouped_rdi = (
            Document.objects.filter(status=Document.STATUS_PENDING)
            .values("individual__registration_data_import")
            .annotate(count=Count("individual__registration_data_import"))
        )
        rdi_ids = [x["individual__registration_data_import"] for x in grouped_rdi if x is not None]
        for rdi in RegistrationDataImport.objects.filter(id__in=rdi_ids).order_by("created_at"):
            with transaction.atomic():
                documents_query = Document.objects.filter(
                    status=Document.STATUS_PENDING, individual__registration_data_import=rdi
                )
                HardDocumentDeduplication().deduplicate(
                    documents_query,
                    registration_data_import=rdi,
                )

        with transaction.atomic():
            documents_query = Document.objects.filter(
                status=Document.STATUS_PENDING, individual__registration_data_import__isnull=True
            )
            HardDocumentDeduplication().deduplicate(
                documents_query,
            )
    return True


@app.task
@log_start_and_end
@sentry_tags
def check_rdi_import_periodic_task(business_area_slug: Optional[str] = None) -> bool:
    with cache.lock(
        f"check_rdi_import_periodic_task_{business_area_slug}",
        blocking_timeout=60 * 5,
        timeout=60 * 60 * 1,
    ) as locked:
        if not locked:
            raise Exception("cannot set lock on check_rdi_import_periodic_task")
        from hct_mis_api.apps.utils.celery_manager import (
            RegistrationDataXlsxImportCeleryManager,
        )

        business_area = BusinessArea.objects.filter(slug=business_area_slug).first()
        manager = RegistrationDataXlsxImportCeleryManager(business_area=business_area)
        manager.execute()
        return True


@app.task
@sentry_tags
def remove_old_rdi_links_task(page_count: int = 100) -> None:
    """This task removes linked RDI Datahub objects for households and related objects (individuals, documents etc.)"""

    from datetime import timedelta

    from constance import config

    days = config.REMOVE_RDI_LINKS_TIMEDELTA
    try:
        # Get datahub_ids older than 3 months which have status other than MERGED
        unmerged_rdi_datahub_ids = list(
            RegistrationDataImport.objects.filter(
                created_at__lte=timezone.now() - timedelta(days=days),
                status__in=[
                    RegistrationDataImport.IN_REVIEW,
                    RegistrationDataImport.DEDUPLICATION_FAILED,
                    RegistrationDataImport.IMPORT_ERROR,
                    RegistrationDataImport.MERGE_ERROR,
                ],
            ).values_list("datahub_id", flat=True)
        )

        i, count = 0, len(unmerged_rdi_datahub_ids) // page_count
        while i <= count:
            logger.info(f"Page {i}/{count} processing...")
            rdi_datahub_ids_page = unmerged_rdi_datahub_ids[i * page_count : (i + 1) * page_count]

            ImportedHousehold.objects.filter(registration_data_import_id__in=rdi_datahub_ids_page).delete()

            RegistrationDataImport.objects.filter(datahub_id__in=rdi_datahub_ids_page).update(erased=True)
            i += 1

        logger.info(
            f"Data links for datahubs: {''.join([str(_id) for _id in unmerged_rdi_datahub_ids])} removed successfully"
        )
    except Exception:
        logger.error("Removing old RDI objects failed")
        raise
