from datetime import datetime
from time import sleep

import pytest
from dateutil.relativedelta import relativedelta
from page_object.programme_details.programme_details import ProgrammeDetails
from page_object.programme_management.programme_management import ProgrammeManagement
from selenium.common import TimeoutException

from hct_mis_api.apps.core.fixtures import DataCollectingTypeFactory
from hct_mis_api.apps.core.models import BusinessArea, DataCollectingType
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def social_worker_program() -> Program:
    return get_program_with_dct_type_and_name("Worker Program", "WORK", DataCollectingType.Type.SOCIAL)


@pytest.fixture
def normal_program() -> Program:
    return get_program_with_dct_type_and_name("Normal Program", "NORM", DataCollectingType.Type.STANDARD)


@pytest.fixture
def active_program() -> Program:
    return get_program_with_dct_type_and_name("Active Program", "ACTI", status=Program.ACTIVE)


@pytest.fixture
def draft_program() -> Program:
    return get_program_with_dct_type_and_name("Draft Program", "DRAF", status=Program.DRAFT)


@pytest.fixture
def finished_program() -> Program:
    return get_program_with_dct_type_and_name("Finished Program", "FINI", status=Program.FINISHED)


def get_program_with_dct_type_and_name(
    name: str, programme_code: str, dct_type: str = DataCollectingType.Type.STANDARD, status: str = Program.ACTIVE
) -> Program:
    BusinessArea.objects.filter(slug="afghanistan").update(is_payment_plan_applicable=True)
    dct = DataCollectingTypeFactory(type=dct_type)
    program = ProgramFactory(
        name=name,
        programme_code=programme_code,
        start_date=datetime.now() - relativedelta(months=1),
        end_date=datetime.now() + relativedelta(months=1),
        data_collecting_type=dct,
        status=status,
    )
    sleep(2)
    return program


@pytest.mark.usefixtures("login")
class TestDrawer:
    def test_social_worker_program_drawer_order(
        self,
        social_worker_program: Program,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
    ) -> None:
        pageProgrammeManagement.selectGlobalProgramFilter("Worker Program").click()
        assert "Worker Program" in pageProgrammeDetails.getHeaderTitle().text
        expected_menu_items = [
            "Registration Data Import",
            "People",
            "Program Details",
            "Targeting",
            "Payment Module",
            "Payment Verification",
            "Grievance",
            "Accountability",
            "Programme Users",
            "Program Log",
        ]
        actual_menu_items = pageProgrammeManagement.getDrawerItems().text.split("\n")
        assert expected_menu_items == actual_menu_items

    def test_normal_program_drawer_order(
        self,
        normal_program: Program,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
    ) -> None:
        pageProgrammeManagement.selectGlobalProgramFilter("Normal Program").click()
        assert "Normal Program" in pageProgrammeDetails.getHeaderTitle().text
        expected_menu_items = [
            "Registration Data Import",
            "Program Population",
            "Program Details",
            "Targeting",
            "Payment Module",
            "Payment Verification",
            "Grievance",
            "Accountability",
            "Programme Users",
            "Program Log",
        ]
        actual_menu_items = pageProgrammeManagement.getDrawerItems().text.split("\n")
        assert expected_menu_items == actual_menu_items

    def test_all_program_drawer_order(
        self,
        social_worker_program: Program,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
    ) -> None:
        expected_menu_items = [
            "Country Dashboard",
            "Programs",
            "Managerial Console",
            "Grievance",
            "Reporting",
            "Activity Log",
        ]
        actual_menu_items = pageProgrammeManagement.getDrawerItems().text.split("\n")
        assert expected_menu_items == actual_menu_items

    def test_inactive_draft_subheader(
        self,
        draft_program: Program,
        active_program: Program,
        finished_program: Program,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
    ) -> None:
        draft_program_name = draft_program.name
        active_program_name = active_program.name
        finished_program_name = finished_program.name
        # clear_cache
        pageProgrammeManagement.getMenuUserProfile().click()
        pageProgrammeManagement.getMenuItemClearCache().click()

        assert Program.objects.all().count() == 3
        print("==>> ", Program.objects.all(), Program.objects.all().values_list("status", flat=True))
        assert Program.objects.filter(status=Program.ACTIVE).count() == 1
        assert Program.objects.filter(status=Program.DRAFT).count() == 1
        assert Program.objects.filter(status=Program.FINISHED).count() == 1

        pageProgrammeManagement.selectGlobalProgramFilter(draft_program_name).click()
        pageProgrammeManagement.selectGlobalProgramFilter(active_program_name).click()
        print("==>>> Programs is there !!!")

        pageProgrammeManagement.selectGlobalProgramFilter(draft_program_name).click()
        assert draft_program_name in pageProgrammeDetails.getHeaderTitle().text
        assert pageProgrammeDetails.getDrawerInactiveSubheader().text == "program inactive"

        pageProgrammeManagement.selectGlobalProgramFilter(active_program_name).click()
        assert active_program_name in pageProgrammeDetails.getHeaderTitle().text
        with pytest.raises(TimeoutException):
            pageProgrammeDetails.getDrawerInactiveSubheader(timeout=0.05)

        # have to add search for Finished program
        # pageProgrammeManagement.selectGlobalProgramFilter(finished_program_name).click()
        # assert finished_program_name in pageProgrammeDetails.getHeaderTitle().text
        # assert pageProgrammeDetails.getDrawerInactiveSubheader().text == "program inactive"
