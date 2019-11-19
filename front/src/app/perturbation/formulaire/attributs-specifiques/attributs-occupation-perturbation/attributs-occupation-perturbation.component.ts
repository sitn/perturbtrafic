import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { IContact } from 'src/app/models/IContact';
import { Subscription } from 'rxjs';
import { DropDownService } from 'src/app/services/dropdown.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';
import { ITypeOccupation } from 'src/app/models/ITypeOccupation';
import { ISuggestion } from 'src/app/models/ISuggestion';

@Component({
  selector: 'attributs-occupation-perturbation',
  templateUrl: './attributs-occupation-perturbation.component.html',
  styleUrls: ['./attributs-occupation-perturbation.component.less']
})
export class AttributsOccupationPerturbationComponent implements OnInit, OnDestroy {

  @Input() perturbationForm: FormGroup;

  public contacts: IContact[];
  public filteredResponsableOccupation: IContact[];
  public typesOccupations: string[];
  public typesRegulations: ISuggestion[];
  public voiesCondamnees: ISuggestion[];

  subscriptions: Subscription[];

  constructor(
    private dropDownService: DropDownService,
    private navigationService: NavigationService,
    public perturbationFormService: PerturbationFormService) {
    this.subscriptions = [];
    this.typesOccupations = [];
    this.typesRegulations = [];
    this.voiesCondamnees = [];
    this.contacts = [...this.dropDownService.contacts];
    this.filteredResponsableOccupation = [...this.dropDownService.contacts];
  }

  ngOnInit() {
    this.dropDownService.getTypesOccupations();
    this.dropDownService.getTypesRegulations();
    this.dropDownService.getTypesVoiesCondamnees();
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  filterResponsableOccupation(event) {
    this.filteredResponsableOccupation = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredResponsableOccupation.push(contact);
      }
    }
  }

/*   onTypeOccupationChanged(value) {
    this.perturbationFormService.typeOccupation.setValue(value);
  } */

  createNewContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
        this.filteredResponsableOccupation = [...contacts];
      })
    );
    this.subscriptions.push(
      this.dropDownService.typesOccupationsReceived$.subscribe(typesOccupations => {
        this.typesOccupations = [...typesOccupations];
      })
    );
    this.subscriptions.push(
      this.dropDownService.regulationsReceived$.subscribe(regulations => {
        this.typesRegulations = [...regulations];
      })
    );
    this.subscriptions.push(
      this.dropDownService.voiesCondamneesReceived$.subscribe(voies => {
        this.voiesCondamnees = [...voies];
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
