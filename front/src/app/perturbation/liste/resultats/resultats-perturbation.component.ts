import { Component, Input, OnChanges, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ExcelExportComponent } from '@progress/kendo-angular-excel-export';
import { GridComponent, GridDataResult } from '@progress/kendo-angular-grid';
import { process, State } from '@progress/kendo-data-query';
import { exportPDF, Group } from '@progress/kendo-drawing';
import { saveAs } from '@progress/kendo-file-saver';
import { LoaderService } from 'src/app/core/loader/loader.service';
import { IResultatPerturbation } from 'src/app/models/IResultatPerturbation';
import { ApiService } from 'src/app/services/api.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'resultats-perturbation',
  templateUrl: './resultats-perturbation.component.html',
  styleUrls: ['./resultats-perturbation.component.less']
})
export class ResultatsPerturbationComponent implements OnInit, OnChanges {

  @ViewChild('occupationGrid', { static: false })
  public occupationGrid: GridComponent;
  @ViewChild('fermetureGrid', { static: false })
  public fermetureGrid: GridComponent;
  @ViewChild('occupationExcel', { static: false })
  public occupationExcel: ExcelExportComponent;
  @ViewChild('fermetureExcel', { static: false })
  public fermetureExcel: ExcelExportComponent;

  @Input() resultats: IResultatPerturbation[];
  filteredResultats: IResultatPerturbation[];
  fermetureResultats: IResultatPerturbation[];
  occupationResultats: IResultatPerturbation[];
  totalResults: number;

  deleteConfirmationOpened = false;
  currentPerturbation: IResultatPerturbation;

  public currentCategoryName: string;

  public gridView: GridDataResult;

  pageSize = 100;

  public state: State = {
    skip: 0,
    filter: {
      logic: 'and',
      filters: [
        /* { field: 'numeroDossier', operator: 'contains' },
        { field: 'commune', operator: 'contains' } */
      ]
    },
    sort: [{
      field: '',
      dir: 'desc'
    }],
    group: []
  };

  public pdfState: State = {
    sort: [{
      field: '',
      dir: 'desc'
    }],
    group: [{ field: 'type' }]
  };

  cols: any[] = [
    { field: 'type', header: 'Type de perturbation', type: 'string', groupable: true },
    { field: 'debut', header: 'Début', type: 'date', format: 'dd.MM.yyyy', groupable: true },
    { field: 'fin', header: 'Fin', type: 'date', format: 'dd.MM.yyyy', groupable: true },
    { field: 'typeEvenement', header: 'Type d\'évènement', type: 'string', groupable: true },
    { field: 'numeroDossier', header: 'N° dossier', type: 'string', groupable: true },
    { field: 'descriptionEvenement', header: 'Évènement', type: 'string', groupable: true },
    { field: 'description', header: 'Description', type: 'string', groupable: true },
    { field: 'etat', header: 'État', type: 'string', groupable: true },
    { field: 'action', header: 'Actions', type: 'action', groupable: false }
  ];

  /*   public rowClass = (context: any): string => {
      if (!this.currentCategoryName) {
        this.currentCategoryName = context.dataItem.type;
      }
      if (this.currentCategoryName !== context.dataItem.type) {
        this.currentCategoryName = context.dataItem.type;
        this.resetCategoryName(context.index);
        return 'test';
      }

      this.resetCategoryName(context.index);
      return '';
    } */

  constructor(private router: Router, private loaderService: LoaderService, private apiService: ApiService,
    private navigationService: NavigationService, public userService: UserService) {
    this.totalResults = 0;
    this.resultats = [];
    this.filteredResultats = [];
    this.occupationResultats = [];
    this.fermetureResultats = [];
    this.gridView = {
      data: [],
      total: 0
    };
  }

  ngOnInit() {
  }

  ngOnChanges() {
    this.filteredResultats = [...this.resultats];

    this.processData(this.state);
  }


  public processData(state: any): void {
    this.state = state;
    const excelState: State = {
      sort: [{
        field: '',
        dir: 'desc'
      }]
    };
    const dataResults = process(this.resultats, this.state);
    const excelResults = process(this.resultats, excelState);
    this.filteredResultats = [...dataResults.data];
    /* console.log('skip : ', this.state.skip);
    this.filteredResultats = dataResults.data.slice(this.state.skip, this.state.skip + this.pageSize);
    this.gridView = {
      data: this.filteredResultats,
      total: this.filteredResultats.length
    }; */
    this.totalResults = this.filteredResultats.length;
    this.occupationResultats = [];
    this.fermetureResultats = [];
    if (excelResults.data && excelResults.data.length > 0) {
      excelResults.data.forEach(resultObject => {
        if (resultObject.type === 'Fermeture') {
          this.fermetureResultats.push(resultObject);
        } else if (resultObject.type === 'Occupation') {
          this.occupationResultats.push(resultObject);
        }
      });
    }

  }


  public formatRows(rows: any): void {
    // const rows = e.workbook.sheets[0].rows;

    let localisationColumnIndex = -1;
    // set alternating row color
    let altIdx = 0;
    rows.forEach((row) => {

      if ((row as any).type === 'header') {
        localisationColumnIndex = row.cells.findIndex(cell => {
          return cell.value === 'Localisation';
        });
      }
      let rowHeight = 20;

      if (row.type === 'data') {

        row.cells.forEach((cell, index) => {
          cell.wrap = true;
          cell.verticalAlign = 'center';
          if (index === localisationColumnIndex) {
            if (cell.value) {
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
  }

  public exportExcel(): void {
    this.loaderService.show();
    Promise.all([this.fermetureExcel.workbookOptions(), this.occupationExcel.workbookOptions()]).then((workbooks) => {
      this.formatRows(workbooks[0].sheets[0].rows);
      this.formatRows(workbooks[1].sheets[0].rows);
      workbooks[0].sheets = workbooks[0].sheets.concat(workbooks[1].sheets);
      workbooks[0].sheets[0].name = 'Fermetures';
      workbooks[0].sheets[1].name = 'Occupations';
      this.fermetureExcel.toDataURL(workbooks[0]).then(url => {
        this.loaderService.hide();
        window.open(url, '_blank');
      });
      // this.fermetureExcel.save(workbooks[0]);
    });
  }

  public exportGrids(): void {
    this.loaderService.show();
    this.occupationResultats = [];
    this.fermetureResultats = [];
    const pdfResults = process(this.resultats, this.pdfState).data;
    if (pdfResults && pdfResults.length > 0) {
      pdfResults.forEach(resultObject => {
        if (resultObject.value === 'Fermeture') {
          this.fermetureResultats = resultObject.items;
        } else if (resultObject.value === 'Occupation') {
          this.occupationResultats = resultObject.items;
        }
      });
    }
    const promises = [];
    promises.push(this.fermetureGrid.drawPDF());
    promises.push(this.occupationGrid.drawPDF());
    Promise.all(promises).then(groups => {
      const rootGroup = new Group({
        pdf: {
          multiPage: true
        }
      });
      groups.forEach((group) => {
        rootGroup.append(...group.children);
      });

      return exportPDF(rootGroup, { paperSize: 'A4', landscape: true });
    }).then(dataUri => {
      this.loaderService.hide();
      saveAs(dataUri, 'Perturbations.pdf');
    });
  }

  /*   private resetCategoryName(index: number): void {
      if (index === this.filteredResultats.length - 1) {
        this.currentCategoryName = undefined;
      }
    }
   */
  public showPerturbation(event) {
    /* this.router.navigate([`/perturbations/formulaire/view/${event.id}`]); */
    window.open(`${window.location.origin}/perturbations/formulaire/view/${event.id}`, '_blank');
  }

  public onDeletePerturbationClick(event) {
    this.deleteConfirmationOpened = true;
    this.currentPerturbation = event;

  }

  public deletePerturbation() {
    this.deleteConfirmationOpened = false;
    this.apiService.deletePerturbation(this.currentPerturbation.id).subscribe(res => {
      if (!res.error) {
        this.deletePerturbationFromResults(this.currentPerturbation.id);
        this.navigationService.openErrorDialog(`La perturbation a été supprimée correctement`, 'Perturbation supprimée');
      } else {
        if (res.code === 403) {

        } else {
          this.navigationService.openErrorDialog(`Une erreur est survenue lors de la suppression : ${res.message}`, 'Erreur');
        }
      }
    });
  }

  public cancelDeletePerturbation() {
    this.deleteConfirmationOpened = false;
  }

  deletePerturbationFromResults(perturbationId) {
    const index = this.resultats.findIndex(val => {
      return val.id === perturbationId;
    });
    if (index > -1) {
      this.resultats.splice(index, 1);
    }
    const indexFiltered = this.filteredResultats.findIndex(val => {
      return val.id === perturbationId;
    });
    if (indexFiltered > -1) {
      this.filteredResultats.splice(indexFiltered, 1);
    }
  }

  public editPerturbation(event) {
    window.open(`${window.location.origin}/perturbations/formulaire/edit/${event.id}`, '_blank');
    /* this.router.navigate([`/perturbations/formulaire/edit/${event.id}`]); */
  }

  public duplicatePerturbation(event) {
    window.open(`${window.location.origin}/perturbations/formulaire/clone/${event.id}`, '_blank');
    /* this.router.navigate([`/perturbations/formulaire/clone/${event.id}`]); */
  }


}
