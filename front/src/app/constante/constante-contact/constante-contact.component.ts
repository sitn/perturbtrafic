import { Component, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { process, State } from '@progress/kendo-data-query';
import { Subscription } from 'rxjs';
import { IContact } from 'src/app/models/IContact';
import { ApiService } from 'src/app/services/api.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'constante-contact',
  templateUrl: './constante-contact.component.html',
  styleUrls: ['./constante-contact.component.less']
})
export class ConstanteContactComponent implements OnInit, OnChanges, OnDestroy {

  private subscriptions: Subscription[];
  contacts: IContact[];
  filteredContacts: IContact[];

  errorRemovingContact = false;

  selectedContact: IContact;

  public state: State = {
    /* filter: {
      logic: 'and',
      filters: [
        { field: 'nom', operator: 'contains' }
        // { field: 'commune', operator: 'contains' }
      ]
    }, */
    sort: [{
      field: 'nom',
      dir: 'asc'
    }],
    group: []
  };

  deleteConfirmationOpened = false;

  constructor(private apiService: ApiService, private navigationService: NavigationService) {
    this.subscriptions = [];
    this.contacts = [];
    this.filteredContacts = [];
  }

  ngOnInit() {
    this.errorRemovingContact = false;
    this.setSubscriptions();
  }

  ngOnChanges() {
    this.filteredContacts = [...this.contacts];

    this.processData(this.state);
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }


  newContact() {
    this.navigationService.openNewContactDialog('NEW', null);
  }

  showContact(item) {
    this.navigationService.openNewContactDialog('READ', item);
  }

  editContact(item) {
    this.navigationService.openNewContactDialog('EDIT', item);
  }

  deleteContact() {
    this.apiService.deleteContact(this.selectedContact.id).subscribe(res => {
      if (res && !res.error) {
        this.deleteConfirmationOpened = false;
        this.apiService.getContacts().subscribe(contacts => {
          this.contacts = contacts;
          this.processData(this.state);
        });
      } else {
        this.errorRemovingContact = true;
      }
    });
  }

  public processData(state: any): void {
    this.state = state;
    const dataResults = process(this.contacts, this.state);
    this.filteredContacts = [...dataResults.data];
    /* console.log('skip : ', this.state.skip);
    this.filteredResultats = dataResults.data.slice(this.state.skip, this.state.skip + this.pageSize);
    this.gridView = {
      data: this.filteredResultats,
      total: this.filteredResultats.length
    }; */
    // this.totalResults = this.filteredResultats.length;

  }

  cancelDeleteContact() {
    this.errorRemovingContact = false;
    this.deleteConfirmationOpened = false;
  }

  public onDeleteContactClick(event) {
    this.deleteConfirmationOpened = true;
    this.selectedContact = event;
  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getContacts().subscribe(contacts => {
        this.contacts = contacts;
        this.processData(this.state);
      })
    );

    this.subscriptions.push(
      this.navigationService.onNewContactDialogClosed$.subscribe(needUpdate => {
        if (needUpdate) {
          this.apiService.getContacts().subscribe(contacts => {
            this.contacts = contacts;
            this.processData(this.state);
          });
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
