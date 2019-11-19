import { Component, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { process, State } from '@progress/kendo-data-query';
import { Subscription } from 'rxjs';
import { IOrganisme } from 'src/app/models/IOrganisme';
import { ApiService } from 'src/app/services/api.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'constante-organisme',
  templateUrl: './constante-organisme.component.html',
  styleUrls: ['./constante-organisme.component.less']
})
export class ConstanteOrganismeComponent implements OnInit, OnDestroy, OnChanges {

  private subscriptions: Subscription[];
  organismes: IOrganisme[];
  filteredOrganismes: IOrganisme[];

  errorRemovingOrganisme = false;

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

  selectedOrganisme: IOrganisme;
  deleteConfirmationOpened = false;

  constructor(private apiService: ApiService, private navigationService: NavigationService) {
    this.subscriptions = [];
    this.organismes = [];
    this.filteredOrganismes = [];
  }

  ngOnInit() {
    this.errorRemovingOrganisme = false;
    this.setSubscriptions();
  }

  ngOnChanges() {
    this.filteredOrganismes = [...this.organismes];

    this.processData(this.state);
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }


  newOrganisme() {
    this.navigationService.openNewOrganismeDialog('NEW', null);
  }

  showOrganisme(item) {
    this.navigationService.openNewOrganismeDialog('READ', item);
  }

  editOrganisme(item) {
    this.navigationService.openNewOrganismeDialog('EDIT', item);
  }

  deleteOrganisme() {
    this.apiService.deleteOrganisme(this.selectedOrganisme.id).subscribe(res => {
      if (res && !res.error) {
        this.deleteConfirmationOpened = false;
        this.apiService.getOrganismes().subscribe(organismes => {
          this.organismes = organismes;
          this.processData(this.state);
        });
      } else {
        this.errorRemovingOrganisme = true;
      }
    });
  }

  public onDeleteOrganismeClick(event) {
    this.deleteConfirmationOpened = true;
    this.selectedOrganisme = event;
  }

  cancelDeleteOrganisme() {
    this.errorRemovingOrganisme = false;
    this.deleteConfirmationOpened = false;
  }

  public processData(state: any): void {
    this.state = state;
    const dataResults = process(this.organismes, this.state);
    this.filteredOrganismes = [...dataResults.data];
    /* console.log('skip : ', this.state.skip);
    this.filteredResultats = dataResults.data.slice(this.state.skip, this.state.skip + this.pageSize);
    this.gridView = {
      data: this.filteredResultats,
      total: this.filteredResultats.length
    }; */
    // this.totalResults = this.filteredResultats.length;

  }

  private setSubscriptions(): void {

    this.subscriptions.push(
      this.apiService.getOrganismes().subscribe(organismes => {
        this.organismes = organismes;
        this.processData(this.state);
      })
    );

    this.subscriptions.push(
      this.navigationService.onNewOrganismeDialogClosed$.subscribe(needUpdate => {
        if (needUpdate) {
          this.apiService.getOrganismes().subscribe(organismes => {
            this.organismes = organismes;
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
