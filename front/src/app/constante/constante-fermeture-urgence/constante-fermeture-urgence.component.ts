import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { IContact, IContactPreavisUrgence } from 'src/app/models/IContact';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';

@Component({
  selector: 'constante-fermeture-urgence',
  templateUrl: './constante-fermeture-urgence.component.html',
  styleUrls: ['./constante-fermeture-urgence.component.less']
})
export class ConstanteFermetureUrgenceComponent implements OnInit {

  preavisContactsUrgence: IContactPreavisUrgence[];
  private subscriptions: Subscription[];

  filteredContacts: IContact[];
  contacts: IContact[];

  currentPreavisContact: IContactPreavisUrgence;
  addContactDialogOpened = false;
  deleteConfirmationOpened = false;

  constructor(private dropDownService: DropDownService, private apiService: ApiService) {
    this.subscriptions = [];
    this.preavisContactsUrgence = [];
    this.filteredContacts = [];
    this.contacts = [];
    this.dropDownService.getContacts();
    this.currentPreavisContact = {
      id_contact: null
    };
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  setCurrentContact(contact) {
    if (contact) {
      this.currentPreavisContact = {
        id_contact: contact.id
      };
    } else {
      this.currentPreavisContact = null;
    }
  }

  addPreavisContact() {
    if (this.currentPreavisContact.id_contact) {
      this.apiService.addNewContactPreavisUrgence(this.currentPreavisContact.id_contact).subscribe(res => {
        if (!res.error) {
          this.apiService.getContactsPreavisUrgence().subscribe(preavisContacts => {
            this.preavisContactsUrgence = [...preavisContacts];
          });
        }
      });
    }
  }

  deletePreavisContact() {
    this.apiService.deleteContactPreavisUrgence(this.currentPreavisContact.id).subscribe(res => {
      if (!res.error) {
        this.apiService.getContactsPreavisUrgence().subscribe(preavisContacts => {
          this.preavisContactsUrgence = [...preavisContacts];
          this.closeDeleteDialog();
        });
      }
    });
  }

  closeDeleteDialog() {
    this.deleteConfirmationOpened = false;
  }

  openDeleteDialog(contact: IContactPreavisUrgence) {
    this.deleteConfirmationOpened = true;
    this.currentPreavisContact = Object.assign({}, contact);
  }


  filterContacts(event) {
    this.filteredContacts = [];
    for (const contact of this.contacts) {
      if (contact.nomComplet.toLowerCase().includes(event.toLowerCase())) {
        this.filteredContacts.push(contact);
      }
    }
  }


  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getContactsPreavisUrgence().subscribe(preavisContacts => {
        this.preavisContactsUrgence = [...preavisContacts];
      })
    );

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe((res: { contacts: IContact[], lastUpdatedId?: number }) => {
        this.contacts = [];
        res.contacts.forEach(contact => {
          if (contact.courriel) {
            this.contacts.push(contact);
          }
        });
        this.filteredContacts = [...res.contacts];
      })
    );
  }

}
