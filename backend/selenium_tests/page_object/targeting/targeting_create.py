from time import sleep

from page_object.base_components import BaseComponents
from selenium.webdriver.remote.webelement import WebElement


class TargetingCreate(BaseComponents):
    # Locators
    targetingCriteria = 'h6[data-cy="title-targeting-criteria"]'
    addCriteriaButton = 'div[data-cy="button-target-population-add-criteria"]'
    addHouseholdRuleButton = '[data-cy="button-household-rule"]'
    addIndividualRuleButton = '[data-cy="button-individual-rule"]'
    addPeopleRuleButton = '[data-cy="button-household-rule"]'
    titlePage = 'h5[data-cy="page-header-title"]'
    fieldName = 'input[data-cy="input-name"]'
    targetingCriteriaAutoComplete = 'input[data-cy="autocomplete-target-criteria-option-{}"]'
    targetingCriteriaValue = '[data-cy="select-filters[{}].value"]'
    targetingCriteriaAddDialogSaveButton = 'button[data-cy="button-target-population-add-criteria"]'
    targetingCriteriaAddDialogSaveButtonEdit = 'button[data-cy="button-target-population-add-criteria"]'
    criteriaContainer = 'div[data-cy="criteria-container"]'
    targetPopulationSaveButton = 'button[data-cy="button-target-population-create"]'
    pageHeaderContainer = 'div[data-cy="page-header-container"]'
    pageHeaderTitle = 'h5[data-cy="page-header-title"]'
    buttonTargetPopulationCreate = 'button[data-cy="button-target-population-create"]'
    inputDivName = 'div[data-cy="input-name"]'
    inputIncludedHouseholdIds = 'div[data-cy="input-included-household-ids"]'
    inputHouseholdids = 'input[data-cy="input-householdIds"]'
    inputIncludedIndividualIds = 'div[data-cy="input-included-individual-ids"]'
    inputIndividualids = 'input[data-cy="input-individualIds"]'
    inputFlagexcludeifonsanctionlist = 'span[data-cy="input-flagExcludeIfOnSanctionList"]'
    inputFlagexcludeifactiveadjudicationticket = 'span[data-cy="input-flagExcludeIfActiveAdjudicationTicket"]'
    iconSelected = '[data-testid="CheckBoxIcon"]'
    iconNotSelected = '[data-testid="CheckBoxOutlineBlankIcon"]'
    inputName = 'input[data-cy="input-name"]'
    divTargetPopulationAddCriteria = 'div[data-cy="button-target-population-add-criteria"]'
    titleExcludedEntries = 'h6[data-cy="title-excluded-entries"]'
    buttonShowHideExclusions = 'button[data-cy="button-show-hide-exclusions"]'
    inputExcludedIds = 'div[data-cy="input-excluded-ids"]'
    inputExcludedids = 'input[data-cy="input-excludedIds"]'
    inputExclusionReason = 'div[data-cy="input-exclusion-reason"]'
    titleAddFilter = 'h6[data-cy="title-add-filter"]'
    autocompleteTargetCriteria = 'div[data-cy="autocomplete-target-criteria"]'
    fieldChooserFilters = 'div[data-cy="field-chooser-filters[0]"]'
    autocompleteTargetCriteriaOption = 'input[data-cy="autocomplete-target-criteria-option-0"]'
    buttonHouseholdRule = 'button[data-cy="button-household-rule"]'
    buttonIndividualRule = 'button[data-cy="button-individual-rule"]'
    buttonTargetPopulationAddCriteria = 'button[data-cy="button-target-population-add-criteria"]'
    buttonSave = 'button[data-cy="button-save"]'
    inputFiltersValueFrom = 'input[data-cy="input-filters[{}].value.from"]'
    inputFiltersValueTo = 'input[data-cy="input-filters[{}].value.to"]'
    inputFiltersValue = 'input[data-cy="input-filters[{}].value"]'
    autocompleteTargetCriteriaValues = 'div[data-cy="autocomplete-target-criteria-values"]'
    selectMany = 'div[data-cy="select-many"]'
    buttonEdit = 'button[data-cy="button-edit"]'

    # Texts
    textTargetingCriteria = "Targeting Criteria"

    def getPageHeaderTitle(self) -> WebElement:
        return self.wait_for(self.pageHeaderTitle)

    def getButtonTargetPopulationCreate(self) -> bool:
        return self.wait_for(self.buttonTargetPopulationCreate)

    def clickButtonTargetPopulationCreate(self) -> bool:
        for _ in range(10):
            self.wait_for(self.buttonTargetPopulationCreate).click()
            try:
                self.wait_for_disappear(self.buttonTargetPopulationCreate)
                break
            except BaseException:
                print("Error: Try again to click Save button during Target Population creation")
        else:
            raise Exception(f"Element {self.buttonTargetPopulationCreate} not found")
        return True

    def getInputName(self) -> WebElement:
        return self.wait_for(self.inputName)

    def getInputIncludedHouseholdIds(self) -> WebElement:
        return self.wait_for(self.inputIncludedHouseholdIds)

    def getInputHouseholdids(self) -> WebElement:
        return self.wait_for(self.inputHouseholdids)

    def getInputIncludedIndividualIds(self) -> WebElement:
        return self.wait_for(self.inputIncludedIndividualIds)

    def getInputIndividualids(self) -> WebElement:
        return self.wait_for(self.inputIndividualids)

    def getInputFlagexcludeifactiveadjudicationticket(self) -> WebElement:
        return self.wait_for(self.inputFlagexcludeifactiveadjudicationticket)

    def getInputFlagexcludeifonsanctionlist(self) -> WebElement:
        return self.wait_for(self.inputFlagexcludeifonsanctionlist)

    def getIconNotSelected(self) -> WebElement:
        return self.wait_for(self.iconNotSelected)

    def getIconSelected(self) -> WebElement:
        return self.wait_for(self.iconSelected)

    def getButtonTargetPopulationAddCriteria(self) -> WebElement:
        return self.wait_for(self.buttonTargetPopulationAddCriteria)

    def getDivTargetPopulationAddCriteria(self) -> WebElement:
        return self.wait_for(self.divTargetPopulationAddCriteria)

    def getTitleExcludedEntries(self) -> WebElement:
        return self.wait_for(self.titleExcludedEntries)

    def getButtonShowHideExclusions(self) -> WebElement:
        return self.wait_for(self.buttonShowHideExclusions)

    def getInputExcludedIds(self) -> WebElement:
        return self.wait_for(self.inputExcludedIds)

    def getInputExcludedids(self) -> WebElement:
        return self.wait_for(self.inputExcludedids)

    def getInputExclusionReason(self) -> WebElement:
        return self.wait_for(self.inputExclusionReason)

    def getButtonHouseholdRule(self) -> WebElement:
        return self.wait_for(self.buttonHouseholdRule)

    def getButtonIndividualRule(self) -> WebElement:
        return self.wait_for(self.buttonIndividualRule)

    def getAutocompleteTargetCriteriaOption(self) -> WebElement:
        return self.wait_for(self.autocompleteTargetCriteriaOption)

    def getTargetingCriteria(self) -> WebElement:
        return self.wait_for(self.targetingCriteria)

    def getTitlePage(self) -> WebElement:
        return self.wait_for(self.titlePage)

    def getAddCriteriaButton(self) -> WebElement:
        return self.wait_for(self.addCriteriaButton)

    def getAddHouseholdRuleButton(self) -> WebElement:
        return self.wait_for(self.addHouseholdRuleButton)

    def getAddIndividualRuleButton(self) -> WebElement:
        return self.wait_for(self.addIndividualRuleButton)

    def getAddPeopleRuleButton(self) -> WebElement:
        return self.wait_for(self.addPeopleRuleButton)

    def getTargetingCriteriaAutoComplete(self, index: int = 0) -> WebElement:
        return self.wait_for(self.targetingCriteriaAutoComplete.format(index))

    def getTargetingCriteriaAutoCompleteIndividual(self, index: int = 0) -> WebElement:
        for _ in range(5):
            if len(self.get_elements(self.targetingCriteriaAutoComplete.format(index))) >= 2:
                break
            sleep(1)
        return self.get_elements(self.targetingCriteriaAutoComplete.format(index))[1]

    def getTargetingCriteriaValue(self, index: int = 0) -> WebElement:
        return self.wait_for(self.targetingCriteriaValue.format(index))

    def getTargetingCriteriaAddDialogSaveButton(self) -> WebElement:
        return self.wait_for(self.targetingCriteriaAddDialogSaveButton)

    def getCriteriaContainer(self) -> WebElement:
        return self.wait_for(self.criteriaContainer)

    def getFieldName(self) -> WebElement:
        return self.wait_for(self.fieldName)

    def getTargetPopulationSaveButton(self) -> WebElement:
        return self.wait_for(self.targetPopulationSaveButton)

    def getButtonSave(self) -> WebElement:
        return self.wait_for(self.buttonSave)

    def getInputFiltersValueFrom(self, fiter_number: int = 0) -> WebElement:
        return self.wait_for(self.inputFiltersValueFrom.format(fiter_number))

    def getInputFiltersValueTo(self, fiter_number: int = 0) -> WebElement:
        return self.wait_for(self.inputFiltersValueTo.format(fiter_number))

    def getInputFiltersValue(self, fiter_number: str) -> WebElement:
        return self.wait_for(self.inputFiltersValue.format(fiter_number))

    def getAutocompleteTargetCriteriaValues(self) -> WebElement:
        return self.wait_for(self.autocompleteTargetCriteriaValues)

    def getSelectMany(self) -> WebElement:
        return self.wait_for(self.selectMany)

    def getButtonEdit(self) -> WebElement:
        return self.wait_for(self.buttonEdit)
