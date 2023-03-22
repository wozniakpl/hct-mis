import abc
import logging
from typing import List, Tuple, Any

from hct_mis_api.apps.core.celery import app
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.registration_datahub.celery_tasks import (
    merge_registration_data_import_task,
    registration_xlsx_import_task,
)
from hct_mis_api.apps.registration_datahub.models import RegistrationDataImportDatahub
from hct_mis_api.apps.targeting.models import TargetPopulation

logger = logging.getLogger(__name__)


class BaseCeleryManager(abc.ABC):
    model: Any = ""
    model_status: str = ""
    task: Any = ""
    lookup: str = ""

    def create_obj_list(self) -> List[str]:
        return list(self.model.objects.filter(status=self.model_status).values_list("id", flat=True))

    @staticmethod
    def get_celery_tasks() -> Tuple[Any, Any, Any]:
        i = app.control.inspect()
        return i.scheduled(), i.active(), i.reserved()

    @abc.abstractmethod
    def create_kwargs(self, ids_to_run: List[str]) -> List:
        pass

    def execute(self) -> None:
        list_to_check = self.create_obj_list()
        celery_ids_list = []
        model_name = self.model.__name__

        for group in self.get_celery_tasks():
            for _, task_list in group.items():
                for task in task_list:
                    task_name = task["name"].split(".")[-1]
                    if task_name == self.task.__name__:
                        celery_ids_list.append(task["kwargs"].get(self.lookup))

        ids_to_run = [rdi_id for rdi_id in list_to_check if rdi_id not in celery_ids_list]
        if not ids_to_run:
            logger.info(f"Found no {model_name} with status {self.model_status}")

        task_kwargs = self.create_kwargs(ids_to_run)
        for kwargs in task_kwargs:
            self.task.delay(**kwargs)
            logger.info(f"Celery task run for {model_name} id: {kwargs[self.lookup]} from periodic task scheduler")


class RdiImportCeleryManager(BaseCeleryManager):
    model = RegistrationDataImport
    model_status = RegistrationDataImport.IMPORTING
    task = registration_xlsx_import_task
    lookup = "registration_data_import_id"

    def create_kwargs(self, ids_to_run: List[str]) -> List:
        registration_xlsx_import_task_kwargs = []
        for rdi_id in ids_to_run:
            rdi = RegistrationDataImport.objects.get(id=rdi_id)
            rdi_datahub = RegistrationDataImportDatahub.objects.get(id=str(rdi.datahub_id))
            kwargs = {
                "registration_data_import_id": str(rdi_datahub.id),
                "import_data_id": str(rdi_datahub.import_data_id),
                "business_area_id": str(rdi.business_area.id),
            }
            registration_xlsx_import_task_kwargs.append(kwargs)
        return registration_xlsx_import_task_kwargs


class RdiMergeCeleryManager(BaseCeleryManager):
    model = RegistrationDataImport
    model_status = RegistrationDataImport.MERGING
    task = merge_registration_data_import_task
    lookup = "registration_data_import_id"

    def create_kwargs(self, ids_to_run: List[str]) -> List:
        merge_registration_data_import_task_kwargs = []
        for rdi_id in ids_to_run:
            merge_registration_data_import_task_kwargs.append({"registration_data_import_id": str(rdi_id)})
        return merge_registration_data_import_task_kwargs


class SendTPCeleryManager(BaseCeleryManager):
    model = TargetPopulation

    def create_kwargs(self, ids_to_run: List[str]) -> List:
        pass


rdi_import_celery_manager = RdiImportCeleryManager()
rdi_merge_celery_manager = RdiMergeCeleryManager()
send_tp_celery_manager = SendTPCeleryManager()
