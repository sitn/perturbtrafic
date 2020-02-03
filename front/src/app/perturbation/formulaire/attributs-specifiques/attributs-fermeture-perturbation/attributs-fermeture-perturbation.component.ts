import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { IContact } from 'src/app/models/IContact';
import { Subscription } from 'rxjs';
import { DropDownService } from 'src/app/services/dropdown.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

@Component({
  selector: 'attributs-fermeture-perturbation',
  templateUrl: './attributs-fermeture-perturbation.component.html',
  styleUrls: ['./attributs-fermeture-perturbation.component.less']
})
export class AttributsFermeturePerturbationComponent implements OnInit, OnDestroy {

  @Input() perturbationForm: FormGroup;

  public contacts: IContact[];
  public filteredResponsableFermeture: IContact[];

  subscriptions: Subscription[];

  dropdownOriginForNewContact: any;

  constructor(
    private dropDownService: DropDownService,
    private navigationService: NavigationService,
    public perturbationFormService: PerturbationFormService) {
    this.subscriptions = [];
    this.contacts = [...this.dropDownService.contacts];
    this.filteredResponsableFermeture = [...this.dropDownService.contacts];
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  filterResponsableFermeture(event) {
    this.filteredResponsableFermeture = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredResponsableFermeture.push(contact);
      }
    }
  }

  createNewContact(dropdownOrigin: any) {
    this.dropdownOriginForNewContact = dropdownOrigin;
    this.navigationService.openNewContactDialog('NEW', null, dropdownOrigin);
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe((res: { contacts: IContact[], lastUpdatedId?: number }) => {
        this.contacts = [...res.contacts];
        this.filteredResponsableFermeture = [...res.contacts];
        if (this.dropdownOriginForNewContact && res.lastUpdatedId) {
          const found = this.contacts.find(val => {
            return val.id === res.lastUpdatedId;
          });
          if (found) {
            this.dropdownOriginForNewContact.setValue(found.id);
          }
        }
        this.dropdownOriginForNewContact = null;
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
