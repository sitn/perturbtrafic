import { Component, Input, OnChanges, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { GridComponent } from '@progress/kendo-angular-grid';
import { orderBy, process, SortDescriptor, State } from '@progress/kendo-data-query';
import { exportPDF, Group } from '@progress/kendo-drawing';
import { saveAs } from '@progress/kendo-file-saver';
import { LoaderService } from 'src/app/core/loader/loader.service';
import { ApiService } from 'src/app/services/api.service';
import { NavigationService } from 'src/app/services/navigation.service';

import { IResultatEvenement } from '../../../models/evenement/IResultatEvenement';
import { ExcelExportComponent, WorkbookSheetRow } from '@progress/kendo-angular-excel-export';

@Component({
  selector: 'resultats-evenement',
  templateUrl: './resultats-evenement.component.html',
  styleUrls: ['./resultats-evenement.component.less']
})
export class ResultatsEvenementComponent implements OnInit, OnChanges {

  @Input() resultats: IResultatEvenement[];

  @ViewChild('exportExcel', { static: false })
  public exportExcel: ExcelExportComponent;

  filteredResultats: IResultatEvenement[];
  totalRecords: number;
  loading = false;

  deleteConfirmationOpened = false;
  currentEvenement: IResultatEvenement;

  public sort: SortDescriptor[] = [{
    field: '',
    dir: 'asc'
  }];

  public state: State = {
    filter: {
      logic: 'and',
      filters: [
        /* { field: 'numeroDossier', operator: 'contains' },
        { field: 'commune', operator: 'contains' } */
      ]
    },
    sort: [{
      field: '',
      dir: 'asc'
    }],
    group: []
  };

  cols: any[] = [
    { field: 'numeroDossier', header: 'N° dossier', type: 'string', filterable: true, show: true, export: true, groupable: true },
    { field: 'localisation', header: 'Localisation', type: 'string', filterable: true, show: true, export: false, groupable: true },
    { field: 'typeEvenement', header: 'Type évènement', type: 'string', filterable: false, show: true, export: true, groupable: true },
    { field: 'prevision', header: 'Prévision', type: 'boolean', filterable: false, show: true, export: true, groupable: true },
    { field: 'libelle', header: 'Libellé', type: 'string', filterable: false, show: true, export: true, groupable: true },
    { field: 'requerant', header: 'Requérant', type: 'string', filterable: false, show: true, export: false, groupable: true },
    { field: 'responsable', header: 'Responsable', type: 'string', filterable: false, show: true, export: false, groupable: true },
    { field: 'division', header: 'Division', type: 'string', filterable: false, show: true, export: true, groupable: true },
    { field: 'debut', header: 'Début', type: 'date', format: 'dd.MM.yyyy', filterable: false, show: true, export: true, groupable: true },
    { field: 'fin', header: 'Fin', type: 'date', format: 'dd.MM.yyyy', filterable: false, show: true, export: true, groupable: true },
    { field: 'action', header: 'Actions', type: 'action', filterable: false, show: true, export: false, groupable: false },
    {
      field: 'localisationImpression',
      header: 'Localisation', type: 'string', filterable: false, show: false, export: true, groupable: false
    },
    {
      field: 'localisationImpressionReperage',
      header: 'Repérage', type: 'string', filterable: false, show: false, export: true, groupable: false
    }
  ];

  constructor(private apiService: ApiService, private router: Router, private navigationService: NavigationService,
    private loaderService: LoaderService) {
    this.filteredResultats = [];
    this.totalRecords = 0;
  }

  ngOnInit() {
  }

  ngOnChanges() {
    this.filteredResultats = [...this.resultats];
    // this.sortResults();
    this.dataStateChange(this.state);
  }

  public sortChange(sort: SortDescriptor[]): void {
    this.sort = sort;
    this.sortResults();
    // this.dataStateChange()
  }

  public sortResults(): void {
    if (this.filteredResultats) {
      this.filteredResultats = orderBy(this.filteredResultats, this.sort);
    }
  }

  public dataStateChange(state: any): void {
    this.state = state;
    const dataResults = process(this.resultats, this.state);
    this.filteredResultats = dataResults.data;
    this.totalRecords = dataResults.total;
  }

  public showEvenement(event) {
    /* this.router.navigate([`/evenements/formulaire/view/${event.id}`]); */
    window.open(`${window.location.origin}/evenements/formulaire/view/${event.id}`, '_blank');
  }

  public onDeleteEvenementClick(event) {
    console.log(event);
    this.deleteConfirmationOpened = true;
    this.currentEvenement = event;

  }

  public deleteEvenement() {
    this.deleteConfirmationOpened = false;
    this.apiService.deleteEvenement(this.currentEvenement.id).subscribe(res => {
      if (!res.error) {
        this.deleteEvenementFromResults(this.currentEvenement.id);
        this.navigationService.openErrorDialog(`L'événement a été supprimé correctement`, 'Evénement supprimé');
      } else {
        this.navigationService.openErrorDialog(`Une erreur est survenue lors de la suppression : ${res.message}`, 'Erreur');
      }
    });
  }

  public cancelDeleteEvenement() {
    this.deleteConfirmationOpened = false;
  }

  deleteEvenementFromResults(evenementId) {
    const index = this.resultats.findIndex(val => {
      return val.id === evenementId;
    });
    if (index > -1) {
      this.resultats.splice(index, 1);
    }
    const indexFiltered = this.filteredResultats.findIndex(val => {
      return val.id === evenementId;
    });
    if (indexFiltered > -1) {
      this.filteredResultats.splice(indexFiltered, 1);
    }
  }

  public editEvenement(event) {
    /* this.router.navigate([`/evenements/formulaire/edit/${event.id}`]); */
    window.open(`${window.location.origin}/evenements/formulaire/edit/${event.id}`, '_blank');
  }

  public duplicateEvenement(event) {
    console.log('duplicate Evenement : ', event);
  }

  public onExcelExport(): void {
    // this.exportExcel.workbookOptions().the
    this.loaderService.show();
    // set alternating row color
    let altIdx = 0;
    Promise.all([this.exportExcel.workbookOptions()]).then((workbooks) => {
      let localisationColumnIndex = -1;
      workbooks[0].sheets[0].rows.forEach((row: WorkbookSheetRow) => {

        if ((row as any).type === 'header') {
          localisationColumnIndex = row.cells.findIndex(cell => {
            return cell.value === 'Localisation';
          });
        }
        let rowHeight = 20;


        if ((row as any).type === 'data') {

          row.cells.forEach((cell, index) => {
            cell.wrap = true;
            cell.verticalAlign = 'center';
            if (index === localisationColumnIndex) {
              if (cell && cell.value) {
                rowHeight = rowHeight * ((cell.value.toString().match(/\r\n/g) || []).length + 1);
              }
            }
            if (typeof (cell.value) === 'boolean') {
              cell.value = cell.value ? 'Oui' : 'Non';
            }
            if (altIdx % 2 !== 0) {
              cell.background = '#aabbcc';
            }
          });
          altIdx++;
        }
        row.height = rowHeight;
      });
      this.exportExcel.toDataURL(workbooks[0]).then(url => {
        this.loaderService.hide();
        window.open(url, '_blank');
      });
    });
  }

  public exportToPDF(grid: GridComponent): void {
    this.loaderService.show();
    grid.drawPDF().then(group => {
      const rootGroup = new Group({
        pdf: {
          multiPage: true
        }
      });
      rootGroup.append(...group.children);
      return exportPDF(rootGroup, { paperSize: 'A4', landscape: true });
    }).then(dataUri => {
      this.loaderService.hide();
      saveAs(dataUri, 'Evenements.pdf');
    });
  }

  addData() {

  }

  printData() {

  }
}
