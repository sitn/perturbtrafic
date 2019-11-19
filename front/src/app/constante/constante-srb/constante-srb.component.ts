import { Component, OnInit } from '@angular/core';
import { IContactAvisPrTouche, IContact } from 'src/app/models/IContact';
import { Subscription } from 'rxjs';
import { DropDownService } from 'src/app/services/dropdown.service';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'constante-srb',
  templateUrl: './constante-srb.component.html',
  styleUrls: ['./constante-srb.component.less']
})
export class ConstanteSrbComponent implements OnInit {

  avisPrTouchesList: IContactAvisPrTouche[];
  private subscriptions: Subscription[];

  filteredContacts: IContact[];
  contacts: IContact[];

  currentPrToucheContact: IContactAvisPrTouche;
  addContactDialogOpened = false;
  deleteConfirmationOpened = false;

  constructor(private dropDownService: DropDownService, private apiService: ApiService) {
    this.subscriptions = [];
    this.avisPrTouchesList = [];
    this.filteredContacts = [];
    this.contacts = [];
    this.dropDownService.getContacts();
    this.currentPrToucheContact = {
      id_contact: null
    };
   }

   ngOnInit() {
    this.setSubscriptions();
  }

  setCurrentContact(contact) {
    if (contact) {
      this.currentPrToucheContact = {
        id_contact: contact.id
      };
    } else {
      this.currentPrToucheContact = null;
    }
  }

  addPreavisContact() {
    if (this.currentPrToucheContact.id_contact) {
      this.apiService.addNewContactAvisPrTouches(this.currentPrToucheContact.id_contact).subscribe(res => {
        if (!res.error) {
          this.apiService.getContactsAvisPrTouches().subscribe(prTouchesList => {
            this.avisPrTouchesList = [...prTouchesList];
          });
        }
      });
    }
  }

  deletePreavisContact() {
    this.apiService.deleteContactAvisPrTouches(this.currentPrToucheContact.id).subscribe(res => {
      if (!res.error) {
        this.apiService.getContactsAvisPrTouches().subscribe(preavisContacts => {
          this.avisPrTouchesList = [...preavisContacts];
          this.closeDeleteDialog();
        });
      }
    });
  }

  closeDeleteDialog() {
    this.deleteConfirmationOpened = false;
  }

  openDeleteDialog(contact: IContactAvisPrTouche) {
    this.deleteConfirmationOpened = true;
    this.currentPrToucheContact = Object.assign({}, contact);
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
      this.apiService.getContactsAvisPrTouches().subscribe(preavisContacts => {
        this.avisPrTouchesList = [...preavisContacts];
      })
    );

    this.subscriptions.push(
      this.dropDownService.contactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
        this.filteredContacts = [...contacts];
      })
    );
  }

}
