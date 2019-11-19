import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { ICommune } from 'src/app/models/ICommune';
import { IContact } from 'src/app/models/IContact';
import { IDestinataireFacturation } from 'src/app/models/IDestinataireFacturation';
import { ILocalite, ILocaliteNPA } from 'src/app/models/ILocalite';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { DropDownService } from 'src/app/services/dropdown.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'attributs-autre-evenement',
  templateUrl: './attributs-autre-evenement.component.html',
  styleUrls: ['./attributs-autre-evenement.component.less']
})
export class AttributsAutreEvenementComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[];

  public organismes: IOrganisme[];
  public contacts: IContact[];
  public localites: ILocaliteNPA[];
  public communes: ICommune[];
  public facturations: IDestinataireFacturation[];

  public filteredMaitreOuvrage: IOrganisme[];
  public filteredEntrepreneur: IOrganisme[];
  public filteredDirectionLocale: IContact[];
  public filteredResponsableTravaux: IContact[];

  public filteredOuvrageLocalites: ILocaliteNPA[];
  public filteredEntrepreneurLocalites: ILocaliteNPA[];

  public filteredCommunes: ICommune[];

  public filteredFacturations: IDestinataireFacturation[];



  constructor(private navigationService: NavigationService, private dropDownService: DropDownService,
    public evenementFormService: EvenementFormService) {
    this.subscriptions = [];

    this.organismes = [...this.dropDownService.organismes];
    this.contacts = [...this.dropDownService.contacts];
    this.localites = [...this.dropDownService.localitesNPA];
    this.communes = [...this.dropDownService.communes];
    this.facturations = [...this.dropDownService.destinatairesFacturations];

    this.filteredDirectionLocale = [...this.dropDownService.contacts];
    this.filteredResponsableTravaux = [...this.dropDownService.contacts];

    this.filteredMaitreOuvrage = [...this.dropDownService.organismes];
    this.filteredEntrepreneur = [...this.dropDownService.organismes];

    this.filteredOuvrageLocalites = [...this.dropDownService.localitesNPA];
    this.filteredEntrepreneurLocalites = [...this.dropDownService.localitesNPA];


    this.filteredCommunes = [...this.dropDownService.communes];

    this.filteredFacturations = [...this.dropDownService.destinatairesFacturations];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }


  filterMaitreOuvrages(event) {
    this.filteredMaitreOuvrage = [];
    for (const organisme of this.organismes) {
      if (organisme.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredMaitreOuvrage.push(organisme);
      }
    }
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

  filterOuvrageLocalites(event) {
    this.filteredOuvrageLocalites = [];
    for (const localite of this.localites) {
      if (localite.npa_nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredOuvrageLocalites.push(localite);
      }
    }
  }

  filterEntrepreneurLocalites(event) {
    this.filteredEntrepreneurLocalites = [];
    for (const localite of this.localites) {
      if (localite.npa_nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredEntrepreneurLocalites.push(localite);
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



  createNewContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  createNewOrganisme() {
    this.navigationService.openNewOrganismeDialog('NEW', null);
  }

  setMaitreOuvrageValues(organisme: IOrganisme) {
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.nom.setValue(organisme.nom);
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.adresse.setValue(organisme.adresse);
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.localite.setValue(organisme.localite);
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.telephone.setValue(organisme.telephone);
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.fax.setValue(organisme.fax);
    this.evenementFormService.autreMaitreOuvrageContactInfos.controls.courriel.setValue(organisme.courriel);
  }

  setEntrepreneurValues(organisme: IOrganisme) {
    this.evenementFormService.autreEntrepreneurContactInfos.controls.nom.setValue(organisme.nom);
    this.evenementFormService.autreEntrepreneurContactInfos.controls.adresse.setValue(organisme.adresse);
    this.evenementFormService.autreEntrepreneurContactInfos.controls.localite.setValue(organisme.localite);
    this.evenementFormService.autreEntrepreneurContactInfos.controls.telephone.setValue(organisme.telephone);
    this.evenementFormService.autreEntrepreneurContactInfos.controls.fax.setValue(organisme.fax);
    this.evenementFormService.autreEntrepreneurContactInfos.controls.courriel.setValue(organisme.courriel);
  }

  setDirectionLocale(contact: IContact) {
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.nom.setValue(contact.nom);
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.prenom.setValue(contact.prenom);
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.mobile.setValue(contact.mobile);
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.telephone.setValue(contact.telephone);
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.fax.setValue(contact.fax);
    this.evenementFormService.autreDirectionLocaleContactInfos.controls.courriel.setValue(contact.courriel);
  }

  setResponsableTravaux(contact: IContact) {
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.nom.setValue(contact.nom);
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.prenom.setValue(contact.prenom);
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.mobile.setValue(contact.mobile);
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.telephone.setValue(contact.telephone);
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.fax.setValue(contact.fax);
    this.evenementFormService.autreResponsableTravauxContactInfos.controls.courriel.setValue(contact.courriel);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
      })
    );

    this.subscriptions.push(
      this.dropDownService.organismesReceived$.subscribe(organismes => {
        this.organismes = [...organismes];
      })
    );

    this.subscriptions.push(
      this.dropDownService.communesReceived$.subscribe(communes => {
        this.communes = [...communes];
      })
    );

    this.subscriptions.push(
      this.dropDownService.destinatairesFacturationsReceived$.subscribe(facturations => {
        this.facturations = [...facturations];
      })
    );

    this.subscriptions.push(
      this.evenementFormService.autreMaitreOuvrageId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.autreMaitreOuvrageContactInfos.reset();
          this.setMaitreOuvrageValues(val);
          this.evenementFormService.autreMaitreOuvrageContactInfos.disable();
        } else {
          this.evenementFormService.autreMaitreOuvrageContactInfos.reset();
          this.evenementFormService.autreMaitreOuvrageContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.autreResponsableTravauxId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.autreResponsableTravauxContactInfos.reset();
          this.setResponsableTravaux(val);
          this.evenementFormService.autreResponsableTravauxContactInfos.disable();
        } else {
          this.evenementFormService.autreResponsableTravauxContactInfos.reset();
          this.evenementFormService.autreResponsableTravauxContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.autreEntrepreneurId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.autreEntrepreneurContactInfos.reset();
          this.setEntrepreneurValues(val);
          this.evenementFormService.autreEntrepreneurContactInfos.disable();
        } else {
          this.evenementFormService.autreEntrepreneurContactInfos.reset();
          this.evenementFormService.autreEntrepreneurContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.autreDirectionLocaleId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.autreDirectionLocaleContactInfos.reset();
          this.setDirectionLocale(val);
          this.evenementFormService.autreDirectionLocaleContactInfos.disable();
        } else {
          this.evenementFormService.autreDirectionLocaleContactInfos.reset();
          this.evenementFormService.autreDirectionLocaleContactInfos.enable();
        }
      })
    );
  }


  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }

}
