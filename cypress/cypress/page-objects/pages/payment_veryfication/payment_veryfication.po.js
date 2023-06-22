import BaseComponent from "../../base.component";

export default class PaymentVerification extends BaseComponent {
  // Locators
  paymentVerificationTitle = "h5[data-cy='page-header-title']";
  paymentPlanID = 'div[data-cy="filter-search"]';
  status = 'div[data-cy="filter-status"]';
  FSP = 'div[data-cy="filter-fsp"]';
  modality = 'div[data-cy="filter-Modality"]';
  startDate = 'div[data-cy="filter-start-date"]';
  endDate = 'div[data-cy="filter-end-date"]';
  statusOptions = 'li[role="option"]';
  listOfCashPlansTitle = 'h6[data-cy="table-title"]';
  buttonApply = 'button[data-cy="button-filters-apply"]';
  tableTitle = 'table[data-cy="table-title"]';
  tableColumn = 'span[data-cy="table-label"]';
  rows = 'tr[data-cy="cash-plan-table-row"]';

  // Texts
  textTitle = "Payment Verification";
  textTabTitle = "List of Cash Plans";
  textPaymentPlanID = "Cash/Payment Plan ID";
  textStatus = "Status";
  textFSP = "FSP";
  textModality = "Modality";
  textStartDate = "Start Date";
  textEndDate = "End Date";
  textCashPlanID = "Cash Plan ID";
  textVerificationStatus = "Verification Status";
  textCashAmount = "Cash Amount";
  textTimeframe = "Timeframe";
  textLastModifiedDate = "Last Modified Date";

  // Elements
  getPaymentVerificationTitle = () => cy.get(this.paymentVerificationTitle);
  getListOfCashPlansTitle = () => cy.get(this.listOfCashPlansTitle);
  getPaymentPlanID = () => cy.get(this.paymentPlanID).eq(0);
  getStatus = () => cy.get(this.status);
  getFSP = () => cy.get(this.FSP);
  getModality = () => cy.get(this.modality);
  getStartDate = () => cy.get(this.startDate);
  getEndDate = () => cy.get(this.endDate);
  getTable = () => cy.get(this.tableTitle);
  getCashPlanID = () => cy.get(this.tableColumn).eq(0);
  getVerificationStatus = () => cy.get(this.tableColumn).eq(1);
  getCashAmount = () => cy.get(this.tableColumn).eq(2);
  getTimeFrame = () => cy.get(this.tableColumn).eq(3);
  getLastModifiedDate = () => cy.get(this.tableColumn).eq(4);
  getCashPlanRows = () => cy.get(this.rows);
  getStatusOption = () => cy.get(this.statusOptions);
  getApply = () => cy.get(this.buttonApply);

  checkPaymentVerificationTitle() {
    return this.getPaymentVerificationTitle().contains(this.textTitle);
  }

  checkListOfCashPlansTitle() {
    return this.getListOfCashPlansTitle().contains(this.textTabTitle);
  }

  checkAllSearchFieldsVisible() {
    this.getPaymentPlanID().should("be.visible");
    this.getPaymentPlanID().get("span").contains(this.textPaymentPlanID);
    this.getStatus().should("be.visible");
    this.getStatus().get("span").contains(this.textStatus);
    this.getFSP().should("be.visible");
    this.getFSP().get("span").contains(this.textFSP);
    this.getModality().should("be.visible");
    this.getModality().get("span").contains(this.textModality);
    this.getStartDate().should("be.visible");
    this.getStartDate().get("span").contains(this.textStartDate);
    this.getEndDate().should("be.visible");
    this.getEndDate().get("span").contains(this.textEndDate);
  }

  checkCashPlansTableVisible() {
    this.getTable().should("be.visible");
    this.getCashPlanID().should("be.visible").contains(this.textCashPlanID);
    this.getVerificationStatus()
      .should("be.visible")
      .contains(this.textVerificationStatus);
    this.getCashAmount().should("be.visible").contains(this.textCashAmount);
    this.getTimeFrame().should("be.visible").contains(this.textTimeframe);
    this.getLastModifiedDate()
      .scrollIntoView()
      .should("be.visible")
      .contains(this.textLastModifiedDate);
  }

  countCashPlanArray() {
    return Array.from(Array(1).keys());
  }

  chooseCashPlan(row) {
    return this.getCashPlanRows().eq(row);
  }

  selectStatus(status) {
    this.getStatus().click();
    this.getStatusOption().contains(status).click();
    this.getStatusOption().contains(status).type("{esc}");
    this.getApply().click();
  }
}
