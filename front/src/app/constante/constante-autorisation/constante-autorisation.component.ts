import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { IContact, IContactAutorisation } from 'src/app/models/IContact';
import { Subscription } from 'rxjs';
import { UserService } from 'src/app/services/user.service';
import { IUser } from 'src/app/models/IUser';

@Component({
  selector: 'constante-autorisation',
  templateUrl: './constante-autorisation.component.html',
  styleUrls: ['./constante-autorisation.component.less']
})
export class ConstanteAutorisationComponent implements OnInit {

  private subscriptions: Subscription[];

  autorisationsDonneesContacts: IContactAutorisation[];
  autorisationsRecuesContacts: IContactAutorisation[];
  filteredContacts: IContact[];
  contacts: IContact[];

  currentAutorisationContact: IContactAutorisation;
  editContactAutorisationOpened = false;
  addContactAutorisationOpened = false;
  deleteConfirmationOpened = false;

  constructor(private apiService: ApiService, private dropDownService: DropDownService, private userService: UserService) {
    this.subscriptions = [];
    this.autorisationsDonneesContacts = [];
    this.autorisationsRecuesContacts = [];
    this.filteredContacts = [];
    this.contacts = [];
    this.dropDownService.getContactsByEntity(this.userService.currentUser.currentEntity.id);
  }

  ngOnInit() {
    this.setSubscriptions();
  }

  addAutorisationContact() {
    if (this.currentAutorisationContact.id_contact) {
      this.apiService.addNewContactAutorisation(this.currentAutorisationContact).subscribe(res => {
        if (!res.error) {
          this.apiService.getAutorisationsAccordees(this.userService.currentUser.currentEntity.id).subscribe(autorisationsContacts => {
            this.autorisationsDonneesContacts = [...autorisationsContacts];
            this.closeCreationDialog();
          });
        }
      });
    }
  }

  updateAutorisationContact() {
    this.apiService.updateContactAutorisation(this.currentAutorisationContact).subscribe(res => {
      if (!res.error) {
        this.apiService.getAutorisationsAccordees(this.userService.currentUser.currentEntity.id).subscribe(autorisationsContacts => {
          this.autorisationsDonneesContacts = [...autorisationsContacts];
          this.closeEditionDialog();
        });
      }
    });
  }

  deleteAutorisationContact() {
    this.apiService.deleteContactAutorisation(this.currentAutorisationContact.id).subscribe(res => {
      if (!res.error) {
        this.apiService.getAutorisationsAccordees(this.userService.currentUser.currentEntity.id).subscribe(autorisationContacts => {
          this.autorisationsDonneesContacts = [...autorisationContacts];
          this.closeDeleteDialog();
        });
      }
    });
  }

  closeDeleteDialog() {
    this.deleteConfirmationOpened = false;
  }

  openDeleteDialog(contact: IContactAutorisation) {
    this.deleteConfirmationOpened = true;
    this.currentAutorisationContact = Object.assign({}, contact);
  }

  openEditionDialog(contact: IContactAutorisation) {
    this.editContactAutorisationOpened = true;
    this.currentAutorisationContact = Object.assign({}, contact);
  }

  closeEditionDialog() {
    this.editContactAutorisationOpened = false;
  }

  openCreationDialog() {
    this.addContactAutorisationOpened = true;
    this.currentAutorisationContact = {
      autorisation_lecture: true,
      autorisation_modification: true,
      autorisation_suppression: true,
      id_contact: null,
      id_delegant: null
    };
  }

  closeCreationDialog() {
    this.addContactAutorisationOpened = false;
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
      this.apiService.getAutorisationsAccordees(this.userService.currentUser.currentEntity.id).subscribe(autorisationsContacts => {
        this.autorisationsDonneesContacts = [...autorisationsContacts];
      })
    );

    this.subscriptions.push(
      this.apiService.getAutorisationsRecues().subscribe(autorisationsContacts => {
        this.autorisationsRecuesContacts = [...autorisationsContacts];
      })
    );

    this.subscriptions.push(
      this.dropDownService.entityContactReceived$.subscribe(contacts => {
        this.contacts = [...contacts];
        this.filteredContacts = [...contacts];
      })
    );

    this.subscriptions.push(this.userService.userState
      .subscribe((user: IUser) => {
        this.apiService.getAutorisationsAccordees(this.userService.currentUser.currentEntity.id).subscribe(autorisationsContacts => {
          this.autorisationsDonneesContacts = [...autorisationsContacts];
        });
        this.dropDownService.getContactsByEntity(this.userService.currentUser.currentEntity.id);
      })
    );
  }


}
