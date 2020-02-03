import { Component, Input, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { IContact, IContactPreavis } from 'src/app/models/IContact';
import { ApiService } from 'src/app/services/api.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'avis-perturbation',
  templateUrl: './avis-perturbation.component.html',
  styleUrls: ['./avis-perturbation.component.less']
})
export class AvisPerturbationComponent implements OnInit, OnDestroy, OnChanges {

  @Input() perturbationPreavis: IContact[];

  subscriptions: Subscription[];
  potentialPreavisList: IContactPreavis[];
  fullPreavisList: IContactPreavis[];

  constructor(public perturbationFormService: PerturbationFormService, public apiService: ApiService, private userService: UserService) {
    this.subscriptions = [];
    this.potentialPreavisList = [];
    this.fullPreavisList = [];
  }

  ngOnInit() {
    this.subscriptions = [];
    this.potentialPreavisList = [];
    this.fullPreavisList = [];
    this.setSubscriptions();
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  ngOnChanges() {

  }

  getCheckedContacts(): number[] {
    const contacts = [];
    this.potentialPreavisList.forEach(contact => {
      if (contact.checked) {
        contacts.push(contact.id_contact);
      }
    });
    return contacts;
  }

  setCheckedContacts(contacts: IContact[], perturbationType: number): void {
    this.updatePreavisList(perturbationType);
    if (contacts && contacts.length > 0) {
      contacts.forEach(contact => {
        const contactIndex = this.potentialPreavisList.findIndex((val, index) => {
          return val.id_contact === contact.id;
        });
        if (contactIndex > -1) {
          this.potentialPreavisList[contactIndex].checked = true;
        }
      });
    }
  }

  updatePreavisList(perturbationType?: number) {

    let pertType = perturbationType;
    if (!pertType && this.perturbationFormService.perturbationForm &&
      this.perturbationFormService.perturbationForm.get('type').value !== null) {
      pertType = this.perturbationFormService.perturbationForm.get('type').value;
    }
    // Fermeture
    this.potentialPreavisList = [];
    if (pertType === 1) {
      this.fullPreavisList.forEach(preavisContact => {
        if (preavisContact.envoi_auto_fermeture) {
          this.potentialPreavisList.push(preavisContact);
        }
      });
    } else if (pertType === 2) {
      this.fullPreavisList.forEach(preavisContact => {
        if (preavisContact.envoi_auto_occupation) {
          this.potentialPreavisList.push(preavisContact);
        }
      });
    }
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getContactsPreavis(this.userService.currentUser.currentEntity.id).subscribe((data: IContactPreavis[]) => {
        this.fullPreavisList = [...data];
        this.updatePreavisList();
      })
    );

    this.subscriptions.push(
      this.perturbationFormService.typePerturbation.valueChanges.subscribe(val => {
        this.updatePreavisList(val);
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
