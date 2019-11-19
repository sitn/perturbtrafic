import { Component, OnChanges, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { ICommune } from 'src/app/models/ICommune';
import { IContact } from 'src/app/models/IContact';
import { IDestinataireFacturation } from 'src/app/models/IDestinataireFacturation';
import { ILocalite, ILocaliteNPA } from 'src/app/models/ILocalite';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { DropDownService } from 'src/app/services/dropdown.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { IPlanTypeFouille } from 'src/app/models/evenement/IFouilleEvenement';

@Component({
  selector: 'attributs-fouille-evenement',
  templateUrl: './attributs-fouille-evenement.component.html',
  styleUrls: ['./attributs-fouille-evenement.component.less']
})
export class AttributsFouilleEvenementComponent implements OnInit, OnChanges {

  private subscriptions: Subscription[];

  public organismes: IOrganisme[];
  public contacts: IContact[];
  public localites: string[];
  public communes: ICommune[];
  public facturations: IDestinataireFacturation[];
  public plansType: IPlanTypeFouille[];

  public filteredMaitreOuvrage: IOrganisme[];
  public filteredEntrepreneur: IOrganisme[];
  public filteredDirectionLocale: IContact[];
  public filteredResponsableTravaux: IContact[];

  public filteredOuvrageLocalites: string[];
  public filteredEntrepreneurLocalites: string[];

  public filteredCommunes: ICommune[];

  public filteredFacturations: IDestinataireFacturation[];



  constructor(private dropDownService: DropDownService, private navigationService: NavigationService,
    public evenementFormService: EvenementFormService) {
    this.subscriptions = [];

    this.organismes = [...this.dropDownService.organismes];
    this.contacts = [...this.dropDownService.contacts];
    this.localites = [...this.dropDownService.localitesPrimitiveNPA];
    this.communes = [...this.dropDownService.communes];
    this.facturations = [...this.dropDownService.destinatairesFacturations];

    this.filteredDirectionLocale = [...this.dropDownService.contacts];
    this.filteredResponsableTravaux = [...this.dropDownService.contacts];

    this.filteredMaitreOuvrage = [...this.dropDownService.organismes];
    this.filteredEntrepreneur = [...this.dropDownService.organismes];

    this.filteredOuvrageLocalites = [...this.dropDownService.localitesPrimitiveNPA];
    this.filteredEntrepreneurLocalites = [...this.dropDownService.localitesPrimitiveNPA];

    this.filteredCommunes = [...this.dropDownService.communes];

    this.filteredFacturations = [...this.dropDownService.destinatairesFacturations];

    this.plansType = [...this.dropDownService.plansTypeFouille];
    this.dropDownService.getPlansTypeFouille();
  }

  ngOnInit() {

    this.setSubscriptions();
  }

  ngOnChanges() {
    console.log('salut');
    // this.setSubscriptions();
  }


  createNewContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  createNewOrganisme() {
    this.navigationService.openNewOrganismeDialog('NEW', null);
  }

  filterMaitreOuvrages(event) {
    this.filteredMaitreOuvrage = [];
    for (const organisme of this.organismes) {
      if (organisme.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredMaitreOuvrage.push(organisme);
      }
    }
  }

  setMaitreOuvrageValues(organisme: IOrganisme) {
    console.log(organisme);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.nom.setValue(organisme.nom);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.adresse.setValue(organisme.adresse);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.localite.setValue(organisme.localite);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.telephone.setValue(organisme.telephone);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.fax.setValue(organisme.fax);
    this.evenementFormService.fouilleMaitreOuvrageContactInfos.controls.courriel.setValue(organisme.courriel);
  }

  setEntrepreneurValues(organisme: IOrganisme) {
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.nom.setValue(organisme.nom);
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.adresse.setValue(organisme.adresse);
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.localite.setValue(organisme.localite);
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.telephone.setValue(organisme.telephone);
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.fax.setValue(organisme.fax);
    this.evenementFormService.fouilleEntrepreneurContactInfos.controls.courriel.setValue(organisme.courriel);
  }

  setDirectionLocale(contact: IContact) {
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.nom.setValue(contact.nom);
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.prenom.setValue(contact.prenom);
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.mobile.setValue(contact.mobile);
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.telephone.setValue(contact.telephone);
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.fax.setValue(contact.fax);
    this.evenementFormService.fouilleDirectionLocaleContactInfos.controls.courriel.setValue(contact.courriel);
  }

  setResponsableTravaux(contact: IContact) {
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.nom.setValue(contact.nom);
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.prenom.setValue(contact.prenom);
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.mobile.setValue(contact.mobile);
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.telephone.setValue(contact.telephone);
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.fax.setValue(contact.fax);
    this.evenementFormService.fouilleResponsableTravauxContactInfos.controls.courriel.setValue(contact.courriel);
  }

  filterEntrepreneur(event) {
    this.filteredEntrepreneur = [];
    for (const organisme of this.organismes) {
      if (organisme.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredEntrepreneur.push(organisme);
      }
    }
  }

  filterDirectionLocale(event) {
    this.filteredDirectionLocale = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredDirectionLocale.push(contact);
      }
    }
  }

  filterResponsableTravaux(event) {
    this.filteredResponsableTravaux = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredResponsableTravaux.push(contact);
      }
    }
  }


  filterCommunes(event) {
    this.filteredCommunes = [];
    for (const commune of this.communes) {
      if (commune.name.toLowerCase().includes(event.toLowerCase())) {
        this.filteredCommunes.push(commune);
      }
    }
  }

  filterFacturation(event) {
    this.filteredFacturations = [];
    for (const facturation of this.facturations) {
      if (facturation.description.toLowerCase().includes(event.toLowerCase())) {
        this.filteredFacturations.push(facturation);
      }
    }
  }

  filterOuvrageLocalites(event) {
    this.filteredOuvrageLocalites = [];
    for (const localite of this.localites) {
      if (localite.toLowerCase().includes(event.toLowerCase())) {
        this.filteredOuvrageLocalites.push(localite);
      }
    }
  }

  filterEntrepreneurLocalites(event) {
    this.filteredEntrepreneurLocalites = [];
    for (const localite of this.localites) {
      if (localite.toLowerCase().includes(event.toLowerCase())) {
        this.filteredEntrepreneurLocalites.push(localite);
      }
    }
  }

  private setSubscriptions(): void {

    this.dropDownService.organismesReceived$.subscribe(organismes => {
      this.organismes = [...organismes];
    });
    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
        this.filteredDirectionLocale = [...contacts];
        this.filteredResponsableTravaux = [...contacts];
      })
    );

    this.subscriptions.push(
      this.dropDownService.organismesReceived$.subscribe(organismes => {
        this.organismes = [...organismes];
        this.filteredEntrepreneur = [...organismes];
        this.filteredMaitreOuvrage = [...organismes];
      })
    );

    this.subscriptions.push(
      this.dropDownService.communesReceived$.subscribe(communes => {
        this.communes = [...communes];
        this.filteredCommunes = [...communes];
      })
    );

    this.subscriptions.push(
      this.dropDownService.destinatairesFacturationsReceived$.subscribe(facturations => {
        this.facturations = [...facturations];
        this.filteredFacturations = [...facturations];
      })
    );

    this.subscriptions.push(
      this.dropDownService.plansTypeFouilleReceived$.subscribe(plans => {
        this.plansType = [...plans];
      })
    );

    this.subscriptions.push(
      this.evenementFormService.fouilleMaitreOuvrageId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.fouilleMaitreOuvrageContactInfos.reset();
          this.setMaitreOuvrageValues(val);
          // this.evenementFormService.fouilleMaitreOuvrageContactInfos.disable();
        } else {
          this.evenementFormService.fouilleMaitreOuvrageContactInfos.reset();
          this.evenementFormService.fouilleMaitreOuvrageContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.fouilleResponsableTravauxId.valueChanges.subscribe(val => {
        this.evenementFormService.fouilleResponsableTravauxContactInfos.reset();
        if (val) {
          this.setResponsableTravaux(val);
          // this.evenementFormService.fouilleResponsableTravauxContactInfos.disable();
        } else {
          this.evenementFormService.fouilleResponsableTravauxContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.fouilleEntrepreneurId.valueChanges.subscribe(val => {
        this.evenementFormService.fouilleEntrepreneurContactInfos.reset();
        if (val) {
          this.setEntrepreneurValues(val);
          // this.evenementFormService.fouilleEntrepreneurContactInfos.disable();
        } else {
          this.evenementFormService.fouilleEntrepreneurContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.fouilleDirectionLocaleId.valueChanges.subscribe(val => {
        this.evenementFormService.fouilleDirectionLocaleContactInfos.reset();
        if (val) {
          this.setDirectionLocale(val);
          // this.evenementFormService.fouilleDirectionLocaleContactInfos.disable();
        } else {
          this.evenementFormService.fouilleDirectionLocaleContactInfos.enable();
        }
      })
    );
  }

}
