import BaseComponent from "../../base.component";

export default class PopulationIndividuals extends BaseComponent {
  // Locators
  titlePage = 'h5[data-cy="page-header-title"]';

  // Texts
  textTitle = "Individuals";

  // Elements
  getTitle = () => cy.get(this.titlePage);

  clickNavIndividuals() {
    this.getMenuButtonProgrammePopulation().click();
    this.getMenuButtonIndividuals().should("be.visible");
    this.getMenuButtonIndividuals().click();
  }
}
