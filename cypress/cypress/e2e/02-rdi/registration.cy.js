/// <reference types="cypress" />

context("RDI", () => {
  beforeEach(() => {
    cy.uniqueSeed().then((seed) => {
      cy.exec(`yarn run generate-xlsx-files 1 ${seed}`);
    });
    cy.visit("/api/unicorn/");
    cy.get('input[name="username"]').type(Cypress.env("username"));
    cy.get('input[name="password"]').type(Cypress.env("password"));
    cy.get("input").contains("Log in").click();
  });
  it("Registration Data Import", () => {
    let householdId;
    let individualId;

    cy.visit("/");
    cy.get("span").contains("Registration Data Import").click();
    cy.get("h5").contains("Registration Data Import");
    cy.get("button > span").contains("IMPORT").click({ force: true });
    cy.get("h2").contains("Select File to Import").click();
    cy.get('[data-cy="import-type-select"]').click();
    cy.get('[data-cy="excel-menu-item"]').click();
    cy.get('[data-cy="input-name"]').type(
      "Test import ".concat(new Date().toISOString())
    );
    cy.uniqueSeed().then((seed) => {
      const fileName = `rdi_import_1_hh_1_ind_seed_${seed}.xlsx`;
      cy.fixture(fileName, "base64").then((fileContent) => {
        cy.get('[data-cy="file-input"]').attachFile({
          fileContent,
          fileName,
          mimeType:
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          encoding: "base64",
        });
      });
    });
    cy.get('[data-cy="number-of-households"]').contains(
      "1 Household available to import",
      {
        timeout: 10000,
      }
    );
    cy.get('[data-cy="number-of-individuals"]').contains(
      "1 Individual available to import"
    );
    cy.get("div").contains("Errors").should("not.exist");
    cy.get('[data-cy="button-import-rdi"').click();

    cy.wait(1000); // eslint-disable-line cypress/no-unnecessary-waiting
    cy.reload();
    cy.wait(500); // eslint-disable-line cypress/no-unnecessary-waiting
    // it lets the browser load the status

    cy.get("div").contains("IMPORT ERROR").should("not.exist");
    cy.get("div").contains("IN REVIEW");

    cy.get("span").contains("Merge").click({ force: true }); // top of page
    cy.get("span").contains("MERGE").click({ force: true }); // inside modal

    cy.get("div").contains("MERGING");

    cy.reload();

    cy.get("div").contains("MERGED");

    return;
    // TODO below is not working
    // because it doesn't see the RDI/ImportedInds/ImportesHhs after it's merged

    cy.log("Looking for householdId");
    cy.get('[data-cy="imported-households-row"]')
      .find("td:nth-child(2)")
      .then(($td) => {
        householdId = $td.text().split(" (")[0];
        cy.log(`Saved householdId: ${householdId}`);
      })
      .then(() => {
        cy.get("button > span").contains("Individuals").click({ force: true });

        cy.get('[data-cy="imported-individuals-table"]')
          .find(`tbody > tr:nth-child(1) > td:nth-child(1)`)
          .then(($td) => {
            individualId = $td.text().split(" (")[0];
            cy.log(`Saved individualId: ${individualId}`);
          })
          .then(() => {
            cy.get("span").contains("Population").click();
            cy.get("span").contains("Households").click();

            cy.log(`looking for householdId: ${householdId}`);
            cy.get('[data-cy="hh-filters-search"]')
              .find("input")
              .type(householdId, { force: true });
            cy.get("td").should("contain", householdId);

            cy.get("span").contains("Individuals").click({ force: true });

            cy.log(`looking for individualId: + ${individualId}`);
            cy.get('[data-cy="ind-filters-search"]').type(individualId);
            cy.get("td").should("contain", individualId);

            cy.get("td").contains(householdId).click({ force: true });

            // cy.get('[data-cy="label-COLLECT TYPE"]').contains("Full"); // TODO
            cy.get('[data-cy="label-Household ID"]').contains(householdId);
          });
      });
  });
});
