import random
from datetime import datetime

from django.conf import settings
from django.core.management import call_command

import pytest
from dateutil.relativedelta import relativedelta
from helpers.date_time_format import FormatTime
from page_object.programme_details.programme_details import ProgrammeDetails
from page_object.programme_management.programme_management import ProgrammeManagement
from selenium.webdriver import Keys

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def create_programs() -> None:
    call_command("loaddata", f"{settings.PROJECT_ROOT}/apps/core/fixtures/data-selenium.json")
    call_command("loaddata", f"{settings.PROJECT_ROOT}/apps/program/fixtures/data-cypress.json")
    yield


@pytest.mark.usefixtures("login")
class TestProgrammeManagement:
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Child Protection",
                    "startDate": FormatTime(1, 5, 2023),
                    "endDate": FormatTime(12, 12, 2033),
                    "dataCollectingType": "Full",
                },
                id="Child Protection & Full",
            ),
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Education",
                    "startDate": FormatTime(11, 12, 2002),
                    "endDate": FormatTime(1, 8, 2043),
                    "dataCollectingType": "Size only",
                },
                id="Education & Size only",
            ),
        ],
    )
    def test_create_programme(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New Programme" in pageProgrammeDetails.getHeaderTitle().text
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "Regular" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert "-" in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "No" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2035),
                    "dataCollectingType": "Partial",
                    "description": f"Text with random {str(random.random())} text",
                    "budget": 1000.99,
                    "administrativeAreas": "Test pass",
                    "populationGoals": "100",
                },
                id="All",
            ),
        ],
    )
    def test_create_programme_optional_values(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputFreqOfPaymentOneOff().click()
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getInputDescription().send_keys(test_data["description"])
        pageProgrammeManagement.getInputBudget().clear()
        pageProgrammeManagement.getInputBudget().send_keys(test_data["budget"])
        pageProgrammeManagement.getInputAdministrativeAreasOfImplementation().send_keys(
            test_data["administrativeAreas"]
        )
        pageProgrammeManagement.getInputPopulation().clear()
        pageProgrammeManagement.getInputPopulation().send_keys(test_data["populationGoals"])
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New Programme" in pageProgrammeDetails.getHeaderTitle().text
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "One-off" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert test_data["administrativeAreas"] in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "Yes" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text
        assert test_data["description"] in pageProgrammeDetails.getLabelDescription().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2042),
                    "dataCollectingType": "Partial",
                },
                id="One-off",
            ),
        ],
    )
    def test_create_programme_Frequency_of_Payment(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys("New Programme")
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputFreqOfPaymentOneOff().click()
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New Programme" in pageProgrammeDetails.getHeaderTitle().text
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "One-off" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert "-" in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "No" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="Yes",
            ),
        ],
    )
    def test_create_programme_Cash_Plus(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New Programme" in pageProgrammeDetails.getHeaderTitle().text
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "Regular" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert "-" in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "Yes" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckProgramme - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="programme_management_page",
            ),
        ],
    )
    def test_create_programme_check(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "Regular" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert "-" in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "Yes" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text
        # Check Programme Management Page
        pageProgrammeManagement.getNavProgrammeManagement().click()
        pageProgrammeManagement.fillFiltersSearch(test_data["program_name"])
        elements = pageProgrammeManagement.getRowByProgramName(test_data["program_name"])
        assert "DRAFT" in elements[1]
        assert "Health" in elements[2]

    def test_create_programme_check_empty_mandatory_fields(self, pageProgrammeManagement: ProgrammeManagement) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getButtonNext().click()
        # Cehck Mandatory fields texts
        assert "Programme Name is required" in pageProgrammeManagement.getLabelProgrammeName().text.split("\n")
        assert "Start Date is required" in pageProgrammeManagement.getLabelStartDate().text
        assert "End Date is required" in pageProgrammeManagement.getLabelEndDate().text
        assert "Sector is required" in pageProgrammeManagement.getLabelSelector().text
        assert "Data Collecting Type is required" in pageProgrammeManagement.getLabelDataCollectingType().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="programme_management_page",
            ),
        ],
    )
    def test_create_programme_delete_partners(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("Only selected partners within the business area")
        pageProgrammeManagement.choosePartnerOption("UNHCR")
        pageProgrammeManagement.getButtonAddPartner().click()
        pageProgrammeManagement.getButtonDelete().click()
        pageProgrammeManagement.getButtonDeletePopup().click()
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        with pytest.raises(Exception):
            assert "UNHCR" in pageProgrammeDetails.getLabelPartnerName().text

    def test_create_programme_cancel_scenario(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getButtonCancel().click()
        assert "Programme Management" in pageProgrammeManagement.getHeaderTitle().text


# ToDo: Check Unicef partner! and delete classes
@pytest.mark.usefixtures("login")
class TestBusinessAreas:
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="programme_management_page",
            ),
        ],
    )
    def test_create_programme_add_partners_Business_Area(
        self,
        change_super_user: None,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
        test_data: dict,
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("Only selected partners within the business area")
        pageProgrammeManagement.choosePartnerOption("UNHCR")
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split(
            "/"
        )  # Check Details page
        assert "UNHCR" in pageProgrammeDetails.getLabelPartnerName().text
        assert "Business Area" in pageProgrammeDetails.getLabelAreaAccess().text

    @pytest.mark.skip(reason="Unstable test")
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="programme_management_page",
            ),
        ],
    )
    def test_copy_programme(
        self,
        change_super_user: None,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
        test_data: dict,
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("None of the partners should have access")
        pageProgrammeManagement.getButtonSave().click()
        pageProgrammeDetails.getCopyProgram().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getButtonSave().click()
        assert "Copy of Programme" in pageProgrammeDetails.getHeaderTitle().text


@pytest.mark.usefixtures("login")
class TestAdminAreas:
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="programme_management_page",
            ),
        ],
    )
    def test_create_programme_add_partners_Admin_Area(
        self,
        change_super_user: None,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
        test_data: dict,
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("Only selected partners within the business area")
        pageProgrammeManagement.choosePartnerOption("UNHCR")
        pageProgrammeManagement.getLabelAdminArea().click()
        pageProgrammeManagement.chooseAreaAdmin1ByName("Baghlan").click()
        # ToDo: Create additional waiting mechanism
        from time import sleep

        sleep(1)
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "UNHCR" in pageProgrammeDetails.getLabelPartnerName().text
        assert "1" in pageProgrammeDetails.getLabelAdminArea1().text
        assert "15" in pageProgrammeDetails.getLabelAdminArea2().text


@pytest.mark.usefixtures("login")
class TestComeBackScenarios:
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                },
                id="Name Change",
            ),
        ],
    )
    def test_create_programme_back_scenarios(
        self,
        change_super_user: None,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
        test_data: dict,
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys("Test Name")
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("Only selected partners within the business area")
        pageProgrammeManagement.choosePartnerOption("UNHCR")
        pageProgrammeManagement.getButtonBack().click()
        assert "Test Name" in pageProgrammeManagement.getInputProgrammeName().get_attribute("value")
        pageProgrammeManagement.getInputProgrammeName().send_keys(Keys.CONTROL, "a")
        pageProgrammeManagement.getInputProgrammeName().send_keys(Keys.DELETE)
        assert "Programme Name is required" in pageProgrammeManagement.getLabelProgrammeName().text.split("\n")
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New Programme" in pageProgrammeDetails.getHeaderTitle().text
        assert "DRAFT" in pageProgrammeDetails.getProgramStatus().text
        assert test_data["startDate"].date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert test_data["endDate"].date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
        assert test_data["selector"] in pageProgrammeDetails.getLabelSelector().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text
        assert "Regular" in pageProgrammeDetails.getLabelFreqOfPayment().text
        assert "-" in pageProgrammeDetails.getLabelAdministrativeAreas().text
        assert "Yes" in pageProgrammeDetails.getLabelCashPlus().text
        assert "0" in pageProgrammeDetails.getLabelProgramSize().text
        assert "UNHCR" in pageProgrammeDetails.getLabelPartnerName().text


@pytest.mark.usefixtures("login")
class TestManualCalendar:
    @pytest.mark.skip(reason="ToDo")
    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "New Programme - " + str(random.random()),
                    "selector": "Health",
                    "dataCollectingType": "Partial",
                },
                id="Change Date",
            ),
        ],
    )
    def test_create_programme_chose_dates_via_calendar(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.chooseInputStartDateViaCalendar(15)
        pageProgrammeManagement.chooseInputEndDateViaCalendar(25)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getButtonNext().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        pageProgrammeManagement.getButtonSave().click()
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert str(datetime.now().strftime("15 %b %Y")) in pageProgrammeDetails.getLabelStartDate().text
        end_date = datetime.now() + relativedelta(months=1)
        assert str(end_date.strftime("25 %b %Y")) in pageProgrammeDetails.getLabelEndDate().text

    @pytest.mark.parametrize(
        "test_data",
        [
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                    "partners_access": "None of the partners should have access",
                },
                id="none_of_the_partners_should_have_access",
            ),
            pytest.param(
                {
                    "program_name": "CheckParents - " + str(random.random()),
                    "selector": "Health",
                    "startDate": FormatTime(1, 1, 2022),
                    "endDate": FormatTime(1, 2, 2032),
                    "dataCollectingType": "Partial",
                    "partners_access": "All partners within the business area",
                },
                id="all_partners_within_the_business_area",
            ),
        ],
    )
    def test_create_programme_accesses(
        self, pageProgrammeManagement: ProgrammeManagement, pageProgrammeDetails: ProgrammeDetails, test_data: dict
    ) -> None:
        # Go to Programme Management
        pageProgrammeManagement.getNavProgrammeManagement().click()
        # Create Programme
        pageProgrammeManagement.getButtonNewProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(test_data["program_name"])
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(test_data["startDate"].numerically_formatted_date)
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(test_data["endDate"].numerically_formatted_date)
        pageProgrammeManagement.chooseOptionSelector(test_data["selector"])
        pageProgrammeManagement.chooseOptionDataCollectingType(test_data["dataCollectingType"])
        pageProgrammeManagement.getInputCashPlus().click()
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram(test_data["partners_access"])
        pageProgrammeManagement.getButtonSave().click()
        assert test_data["partners_access"] in pageProgrammeDetails.getLabelPartnerAccess().text
        assert test_data["dataCollectingType"] in pageProgrammeDetails.getLabelDataCollectingType().text

    def test_edit_programme(
        self,
        create_programs: None,
        pageProgrammeManagement: ProgrammeManagement,
        pageProgrammeDetails: ProgrammeDetails,
    ) -> None:
        pageProgrammeManagement.getNavProgrammeManagement().click()
        pageProgrammeManagement.getTableRowByProgramName("Test Programm").click()

        pageProgrammeManagement.getButtonEditProgram().click()
        pageProgrammeManagement.getInputProgrammeName().send_keys(Keys.CONTROL + "a")
        pageProgrammeManagement.getInputProgrammeName().send_keys("New name after Edit")
        pageProgrammeManagement.getInputProgrammeCode().send_keys(Keys.CONTROL + "a")
        pageProgrammeManagement.getInputProgrammeCode().send_keys("NEW1")
        pageProgrammeManagement.getInputStartDate().click()
        pageProgrammeManagement.getInputStartDate().send_keys(Keys.CONTROL + "a")
        pageProgrammeManagement.getInputStartDate().send_keys(str(FormatTime(1, 1, 2022).numerically_formatted_date))
        pageProgrammeManagement.getInputEndDate().click()
        pageProgrammeManagement.getInputEndDate().send_keys(Keys.CONTROL + "a")
        pageProgrammeManagement.getInputEndDate().send_keys(FormatTime(1, 10, 2022).numerically_formatted_date)
        pageProgrammeManagement.getButtonNext().click()
        pageProgrammeManagement.getAccessToProgram().click()
        pageProgrammeManagement.selectWhoAccessToProgram("None of the partners should have access")
        pageProgrammeManagement.getButtonSave().click()
        programme_creation_url = pageProgrammeManagement.driver.current_url
        # Check Details page
        assert "details" in pageProgrammeDetails.wait_for_new_url(programme_creation_url).split("/")
        assert "New name after Edit" in pageProgrammeDetails.getHeaderTitle().text
        assert FormatTime(1, 1, 2022).date_in_text_format in pageProgrammeDetails.getLabelStartDate().text
        assert FormatTime(1, 10, 2022).date_in_text_format in pageProgrammeDetails.getLabelEndDate().text
