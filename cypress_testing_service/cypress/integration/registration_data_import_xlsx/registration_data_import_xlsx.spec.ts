import {
  Given,
  When,
  And,
  Then,
  Before,
} from 'cypress-cucumber-preprocessor/steps';
import { uuid } from 'uuidv4';
import { WorkBook } from 'xlsx';
import { apiUrl, api } from '../../support/api';
import { overrideSrollingStrategy } from '../../support/utils';

Before(() => {
  overrideSrollingStrategy();
});

Given('the User is viewing the Registration Data Import screen', () => {
  cy.navigateTo('/registration-data-import');

  cy.getByTestId('page-header-container').contains('registration data import', {
    matchCase: false,
  });
});

When('the User starts to import new data', () => {
  cy.getByTestId('page-header-container')
    .getByTestId('button-import')
    .should('be.visible')
    .click();
});

And('the User selects {word} as their import source', (source) => {
  cy.getByTestId('select-import-from').click();

  cy.getByTestId('select-import-from-options')
    .find('ul')
    .contains(source, { matchCase: false })
    .click();
});

And('the User downloads template', () => {
  cy.getByTestId('a-download-template').click();
});

Then('the XLSX file stored in the system is downloaded', () => {
  cy.getByTestId('a-download-template')
    .click()
    .then((anchor) => {
      const url = anchor.attr('href');

      cy.downloadXlsxData(url).parseXlsxData().as('downloadedXlsx');
    });
});

And(
  'the downloaded XLSX file has the Households, Individuals and Choices sheets',
  () => {
    cy.get<{ workbook: WorkBook }>('@downloadedXlsx').should(({ workbook }) => {
      expect(workbook.SheetNames).to.deep.eq([
        'Households',
        'Individuals',
        'Choices',
      ]);
    });
  },
);

Given(
  'the User is prompted to select a file from the Import Excel screen',
  () => {
    cy.navigateTo('/registration-data-import');

    cy.getByTestId('page-header-container').contains(
      'registration data import',
      {
        matchCase: false,
      },
    );

    cy.getByTestId('page-header-container')
      .getByTestId('button-import')
      .should('be.visible')
      .click();
  },
);

And('the User uploads file', () => {
  const path = 'documents/rdi';
  cy.fixture(`${path}/meta`).then(({ valid }) => {
    const { fileName, ...otherMeta } = valid;
    cy.fixture(`${path}/${fileName}`, 'base64').then((fileContent) => {
      // @ts-ignore
      cy.getByTestId('rdi-file-input').upload({
        fileName,
        fileContent,
        encoding: 'base64',
        ...otherMeta,
      });
    });

    cy.getByTestId('loading-container').should('be.visible');
    cy.getByTestId('dialog-root').contains(fileName);
    cy.getByTestId('loading-container', { timeout: 10000 }).should(
      'not.be.visible',
    );
  });
});

And('the file has no errors', () => {
  cy.getByTestId('errors-container').should('not.be.visible');
});

And('the User completes all required fields', () => {
  cy.fixture('rdi').then(({ name }) => {
    const uniqueName = `${name} ${uuid()}`;
    cy.getByTestId('dialog-root').getByTestId('input-name').type(uniqueName);

    cy.wrap(uniqueName).as('uploadedXlsx');
  });
});

And('the User confirms the import', () => {
  cy.getByTestId('dialog-actions-container')
    .getByTestId('button-import')
    .click();
  cy.getByTestId('dialog-root').should('not.be.visible');
});

Then('the User is taken to the Import details screen', () => {
  cy.getByTestId('page-header-container').contains('registration data import', {
    matchCase: false,
  });

  cy.get<string>('@uploadedXlsx').then((uploadName) => {
    cy.getByTestId('page-header-container').contains(uploadName);
  });
});

And('the information from uploaded file is visible', () => {
  // TODO: clarify level of details to be tested
  // TODO: consider getting data from fixtures
  cy.getByTestId('labelized-field-container-households').contains('18');
  cy.getByTestId('labelized-field-container-individuals').contains('72');
});

Given('the User has an RDI import in review', () => {
  cy.getBusinessAreaSlug().then((businessAreaSlug) => {
    const path = 'documents/rdi';
    cy.fixture(`${path}/meta`).then(({ valid }) => {
      const { fileName } = valid;
      cy.fixture(`${path}/${fileName}`, 'base64')
        .then((file) => {
          // https://github.com/abramenal/cypress-file-upload/issues/12
          return Cypress.Blob.base64StringToBlob(
            file,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          );
        })
        .as('blob');
    });

    cy.get<Blob>('@blob').then((blob) => {
      cy.gqlUploadFile(
        apiUrl,
        api.getUploadImportDataXlsxFileOperation(businessAreaSlug),
        blob,
        'valid.xlsx',
      ).as('fileUploadResponse');
    });

    cy.get<{ data: any }>('@fileUploadResponse').then((fileUploadResponse) => {
      const {
        data: {
          uploadImportDataXlsxFile: {
            importData: { id: importDataId },
          },
        },
      } = fileUploadResponse;

      const name = `Automated RDI Import ${uuid()}`;
      api
        .createRegistrationDataImport({
          name,
          businessAreaSlug,
          importDataId,
        })
        .then((response) => {
          const {
            data: {
              createRegistrationDataImport: { registrationDataImport },
            },
          } = response.body;
          cy.wrap(registrationDataImport).as('registrationDataImport');
        });
    });
  });

  cy.get<{ id: string }>('@registrationDataImport').then(({ id }) => {
    cy.navigateTo(`/registration-data-import/${id}`);

    const getStatus = (status: string) => {
      cy.getByTestId('status-container').then(($status) => {
        if ($status.text().toLowerCase().includes(status)) {
          cy.wrap($status).as('status');
          return;
        }

        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(5000);
        cy.reload();
        getStatus(status);
      });
    };

    getStatus('in review');
    cy.get('@status', { timeout: 60000 });
  });
});

And('the User has reviewed all import data content', () => {
  // TODO: add 1-2 assertions to verify
});

When('the User approves the RDI import', () => {
  cy.getByTestId('page-header-container').getByTestId('button-approve').click();
  cy.getByTestId('dialog-actions-container')
    .getByTestId('button-approve')
    .click();
});

Then('the RDI import becomes approved', () => {
  cy.getByTestId('status-container').contains('approved', { matchCase: false });
});

When('the User unapproves the RDI import', () => {
  cy.getByTestId('page-header-container')
    .getByTestId('button-unapprove')
    .click();

  cy.getByTestId('dialog-actions-container')
    .getByTestId('button-unapprove')
    .click();
});

Then('the RDI import changes status to in review', () => {
  cy.getByTestId('status-container').contains('in review', {
    matchCase: false,
  });
});
