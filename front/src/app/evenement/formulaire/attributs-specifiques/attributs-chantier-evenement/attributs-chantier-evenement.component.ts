import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { IContact } from 'src/app/models/IContact';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { DropDownService } from 'src/app/services/dropdown.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { ICategorieChantier } from 'src/app/models/evenement/IChantier';

@Component({
  selector: 'attributs-chantier-evenement',
  templateUrl: './attributs-chantier-evenement.component.html',
  styleUrls: ['./attributs-chantier-evenement.component.less']
})
export class AttributsChantierEvenementComponent implements OnInit, OnDestroy {


  public timeMask = '00:00';
  private subscriptions: Subscription[];

  public organismes: IOrganisme[];
  public contacts: IContact[];

  public categoriesChantier: ICategorieChantier[];

  public filteredMaitreOuvrage: IOrganisme[];
  public filteredEntrepreneur: IOrganisme[];
  public filteredCentraleEnrobage: IOrganisme[];
  public filteredDirectionLocale: IContact[];
  public filteredResponsableTravaux: IContact[];

  public selectedDirectionLocale: IContact;
  public selectedResponsableTravaux: IContact;

  public selectedMaitreOuvrage: IOrganisme;
  public selectedEntrepreneur: IOrganisme;

  chantierEvenementForm: FormGroup;

  dropdownOriginForNewContact: any;

  constructor(private fb: FormBuilder, private navigationService: NavigationService, private dropDownService: DropDownService,
    public evenementFormService: EvenementFormService) {
    this.subscriptions = [];

    this.organismes = [...this.dropDownService.organismes];
    this.filteredMaitreOuvrage = [...this.dropDownService.organismes];
    this.filteredEntrepreneur = [...this.dropDownService.organismes];
    this.filteredCentraleEnrobage = [...this.dropDownService.organismes];

    this.contacts = [...this.dropDownService.contacts];
    this.filteredDirectionLocale = [...this.dropDownService.contacts];
    this.filteredResponsableTravaux = [...this.dropDownService.contacts];

    this.categoriesChantier = [];
    this.dropDownService.getCategoriesChantier();
  }

  ngOnInit() {
    this.dropdownOriginForNewContact = null;
    this.setSubscriptions();
    this.selectedDirectionLocale = this.contacts.find(cont => {
      return cont.id === this.evenementFormService.directionLocale.value;
    });
    this.selectedResponsableTravaux = this.contacts.find(cont => {
      return cont.id === this.evenementFormService.responsableTravaux.value;
    });

    this.selectedMaitreOuvrage = this.organismes.find(org => {
      return org.id === this.evenementFormService.maitreOuvrage.value;
    });
    this.selectedEntrepreneur = this.organismes.find(cont => {
      return cont.id === this.evenementFormService.entrepreneur.value;
    });
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

  filterCentraleEnrobage(event) {
    this.filteredCentraleEnrobage = [];
    for (const organisme of this.organismes) {
      if (organisme.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredCentraleEnrobage.push(organisme);
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

  createNewContact(dropdownOrigin: any) {
    this.dropdownOriginForNewContact = dropdownOrigin;
    this.navigationService.openNewContactDialog('NEW', null, dropdownOrigin);
  }

  createNewOrganisme() {
    this.navigationService.openNewOrganismeDialog('NEW', null);
  }

  private setSubscriptions(): void {

    this.evenementFormService.directionLocale.valueChanges.subscribe(val => {
      this.selectedDirectionLocale = this.contacts.find(cont => {
        return cont.id === val;
      });
    });

    this.evenementFormService.responsableTravaux.valueChanges.subscribe(val => {
      this.selectedResponsableTravaux = this.contacts.find(cont => {
        return cont.id === val;
      });
    });

    this.evenementFormService.maitreOuvrage.valueChanges.subscribe(val => {
      this.selectedMaitreOuvrage = this.organismes.find(org => {
        return org.id === val;
      });
    });

    this.evenementFormService.entrepreneur.valueChanges.subscribe(val => {
      this.selectedEntrepreneur = this.organismes.find(org => {
        return org.id === val;
      });
    });

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe((res: { contacts: IContact[], lastUpdatedId?: number }) => {
        this.contacts = [...res.contacts];
        this.filteredResponsableTravaux = [...res.contacts];
        this.filteredDirectionLocale = [...res.contacts];
        if (this.dropdownOriginForNewContact && res.lastUpdatedId) {
          const found = this.contacts.find(val => {
            return val.id === res.lastUpdatedId;
          });
          if (found) {
            this.dropdownOriginForNewContact.setValue(found.id);
          }
        }
        this.selectedDirectionLocale = this.contacts.find(cont => {
          return cont.id === this.evenementFormService.directionLocale.value;
        });
        this.selectedResponsableTravaux = this.contacts.find(cont => {
          return cont.id === this.evenementFormService.responsableTravaux.value;
        });

        this.dropdownOriginForNewContact = null;
      })
    );

    this.subscriptions.push(
      this.dropDownService.organismesReceived$.subscribe(organismes => {
        this.organismes = [...organismes];
        this.filteredCentraleEnrobage = [...organismes];
        this.filteredEntrepreneur = [...organismes];
        this.filteredMaitreOuvrage = [...organismes];

        this.selectedMaitreOuvrage = this.organismes.find(org => {
          return org.id === this.evenementFormService.maitreOuvrage.value;
        });

        this.selectedEntrepreneur = this.organismes.find(org => {
          return org.id === this.evenementFormService.entrepreneur.value;
        });
      })
    );

    this.subscriptions.push(
      this.dropDownService.categoriesChantierReceived$.subscribe(categories => {
        this.categoriesChantier = [...categories];
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
