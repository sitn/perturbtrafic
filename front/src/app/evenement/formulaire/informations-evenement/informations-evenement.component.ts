import { ChangeDetectorRef, Component, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { Subscription } from 'rxjs';
import { IContact } from 'src/app/models/IContact';
import { ILocalite, ILocaliteNPA } from 'src/app/models/ILocalite';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { ISuggestion } from 'src/app/models/ISuggestion';

@Component({
  selector: 'informations-evenement',
  templateUrl: './informations-evenement.component.html',
  styleUrls: ['./informations-evenement.component.less']
})
export class InformationsEvenementComponent implements OnInit, OnDestroy, OnChanges {

  public source: Array<{ text: string, value: number }> = [
    { text: 'Neuchatel', value: 1 },
    { text: 'Echallens', value: 2 },
    { text: 'Echichens', value: 3 }
  ];

  filteredResponsables: IContact[];

  localites: ILocaliteNPA[];
  filteredLocalites: ILocaliteNPA[];

  requerants: IOrganisme[];
  filteredRequerants: IOrganisme[];
  filteredRequerantLocalites: ILocaliteNPA[];
  contacts: IContact[];
  divisions: ISuggestion[];
  filteredContacts: IContact[];

  public timeMask = '00:00';

  // @Input() evenementForm: FormGroup;
  // @Output() evenementChange = new EventEmitter<IEvenement>();

  /* get numeroDossier() { return this.evenementForm.controls.numeroDossier; }
  get dates() { return this.evenementForm.controls.dates; }
  get typeEvenement() { return (this.evenementForm.controls.type as FormGroup).controls.type; } */

  public data: Array<{ text: string, value: number }>;

  private subscriptions: Subscription[];

  constructor(private apiService: ApiService, private dropDownService: DropDownService,
    private ref: ChangeDetectorRef, public evenementFormService: EvenementFormService, private navigationService: NavigationService) {
    this.subscriptions = [];

    this.contacts = [...this.dropDownService.contacts];
    this.divisions = [...this.dropDownService.divisions];
    this.filteredContacts = [...this.dropDownService.contacts];
    this.filteredRequerants = [...this.dropDownService.organismes];
    this.requerants = [...this.dropDownService.organismes];
    this.localites = [...this.dropDownService.localitesNPA];
    this.filteredLocalites = [...this.dropDownService.localitesNPA];
    this.filteredRequerantLocalites = [...this.dropDownService.localitesNPA];
    this.filteredResponsables = [...this.dropDownService.contacts];
  }

  ngOnInit() {


    this.setSubscriptions();
  }

  ngOnChanges(changes: SimpleChanges) {
    this.ref.detectChanges();
    console.log(changes);
    const eve = this.evenementFormService.evenementForm;
    /* if (this.evenementForm.disabled) {
      this.evenementForm.disable();
    } */
    // this.evenementForm.disable();
    console.log(eve);
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  filterResponsables(event) {
    this.filteredResponsables = [];
    for (const responsable of this.dropDownService.contacts) {
      if (responsable.nom.toLowerCase().includes(event.toLowerCase()) || responsable.prenom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredResponsables.push(responsable);
      }
    }
  }

  filterRequerants(event) {
    this.filteredRequerants = [];
    for (const requerant of this.requerants) {
      if (requerant.nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredRequerants.push(requerant);
      }
    }
  }

  setRequerantValues(organisme: IOrganisme) {
    this.evenementFormService.requerantContactInfos.controls.nom.setValue(organisme.nom);
    this.evenementFormService.requerantContactInfos.controls.adresse.setValue(organisme.adresse);
    this.evenementFormService.requerantContactInfos.controls.localite.setValue(organisme.localite);
    this.evenementFormService.requerantContactInfos.controls.telephone.setValue(organisme.telephone);
    this.evenementFormService.requerantContactInfos.controls.fax.setValue(organisme.fax);
    this.evenementFormService.requerantContactInfos.controls.courriel.setValue(organisme.courriel);
  }

  filterContacts(event) {
    this.filteredContacts = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredContacts.push(contact);
      }
    }
  }

  setContactValues(contact: IContact) {
    this.evenementFormService.personneContactInfos.controls.nom.setValue(contact.nom);
    this.evenementFormService.personneContactInfos.controls.prenom.setValue(contact.prenom);
    this.evenementFormService.personneContactInfos.controls.mobile.setValue(contact.mobile);
    this.evenementFormService.personneContactInfos.controls.telephone.setValue(contact.telephone);
    this.evenementFormService.personneContactInfos.controls.fax.setValue(contact.fax);
    this.evenementFormService.personneContactInfos.controls.courriel.setValue(contact.courriel);
  }

  filterRequerantLocalites(event) {
    this.filteredRequerantLocalites = [];
    for (const localite of this.localites) {
      if (localite.npa_nom.toLowerCase().includes(event.toLowerCase())) {
        this.filteredRequerantLocalites.push(localite);
      }
    }
  }

  createNewOrganisme() {
    this.navigationService.openNewOrganismeDialog('NEW', null);
  }

  createNewContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(data => {
        this.filteredResponsables = data;
        this.filteredContacts = data;
        this.contacts = data;
      })
    );

    this.subscriptions.push(
      this.dropDownService.divisionsReceived$.subscribe(data => {
        this.divisions = data;
      })
    );

    this.subscriptions.push(
      this.dropDownService.organismesReceived$.subscribe(data => {
        this.filteredRequerants = data;
        this.requerants = data;
      })
    );

    this.subscriptions.push(
      this.dropDownService.localitesNPAReceived$.subscribe(data => {
        this.filteredLocalites = data;
        this.filteredRequerantLocalites = data;
        this.localites = data;
      })
    );

    this.subscriptions.push(
      this.evenementFormService.requerantId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.requerantContactInfos.reset();
          this.setRequerantValues(val);
          // this.evenementFormService.requerantContactInfos.disable();
        } else if (this.evenementFormService.mode !== 'READ_ONLY') {
          this.evenementFormService.requerantContactInfos.reset();
          this.evenementFormService.requerantContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.personneContactId.valueChanges.subscribe(val => {
        if (val) {
          this.evenementFormService.personneContactInfos.reset();
          this.setContactValues(val);
        } else if (this.evenementFormService.mode !== 'READ_ONLY') {
          this.evenementFormService.personneContactInfos.reset();
          this.evenementFormService.personneContactInfos.enable();
        }
      })
    );

    this.subscriptions.push(
      this.evenementFormService.dateDebut.valueChanges.subscribe(val => {
        console.log('value debut changed : ', val);
      })
    );

    this.subscriptions.push(
      this.evenementFormService.dateFin.valueChanges.subscribe(val => {
        console.log('value fin changed : ', val);
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
