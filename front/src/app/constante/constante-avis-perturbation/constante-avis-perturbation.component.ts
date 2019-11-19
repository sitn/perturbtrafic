import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { IContact, IContactPreavis } from 'src/app/models/IContact';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';

@Component({
  selector: 'constante-avis-perturbation',
  templateUrl: './constante-avis-perturbation.component.html',
  styleUrls: ['./constante-avis-perturbation.component.less']
})
export class ConstanteAvisPerturbationComponent implements OnInit {

  private subscriptions: Subscription[];

  preavisContacts: IContactPreavis[];
  filteredContacts: IContact[];
  contacts: IContact[];

  currentPreavisContact: IContactPreavis;
  editContactPreavisOpened = false;
  addContactPreavisOpened = false;
  deleteConfirmationOpened = false;

  constructor(private apiService: ApiService, private dropDownService: DropDownService) {
    this.subscriptions = [];
    this.preavisContacts = [];
    this.filteredContacts = [];
    this.contacts = [];
    this.dropDownService.getContacts();
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  addPreavisContact() {
    if (this.currentPreavisContact.id_contact) {
      this.apiService.addNewContactPreavis(this.currentPreavisContact).subscribe(res => {
        if (!res.error) {
          this.apiService.getContactsPreavis().subscribe(preavisContacts => {
            this.preavisContacts = [...preavisContacts];
            this.closeCreationDialog();
          });
        }
      });
    }
  }

  updatePreavisContact() {
    this.apiService.updateContactPreavis(this.currentPreavisContact).subscribe(res => {
      if (!res.error) {
        this.apiService.getContactsPreavis().subscribe(preavisContacts => {
          this.preavisContacts = [...preavisContacts];
          this.closeEditionDialog();
        });
      }
    });
  }

  deletePreavisContact() {
    this.apiService.deleteContactPreavis(this.currentPreavisContact.id).subscribe(res => {
      if (!res.error) {
        this.apiService.getContactsPreavis().subscribe(preavisContacts => {
          this.preavisContacts = [...preavisContacts];
          this.closeDeleteDialog();
        });
      }
    });
  }

  closeDeleteDialog() {
    this.deleteConfirmationOpened = false;
  }

  openDeleteDialog(contact: IContactPreavis) {
    this.deleteConfirmationOpened = true;
    this.currentPreavisContact = Object.assign({}, contact);
  }

  openEditionDialog(contact: IContactPreavis) {
    this.editContactPreavisOpened = true;
    this.currentPreavisContact = Object.assign({}, contact);
  }

  closeEditionDialog() {
    this.editContactPreavisOpened = false;
  }

  openCreationDialog() {
    this.addContactPreavisOpened = true;
    this.currentPreavisContact = {
      envoi_auto_fermeture: true,
      envoi_auto_occupation: true,
      id_contact: null
    };
  }

  closeCreationDialog() {
    this.addContactPreavisOpened = false;
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
      this.apiService.getContactsPreavis().subscribe(preavisContacts => {
        this.preavisContacts = [...preavisContacts];
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
