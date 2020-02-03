import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { IAxeMaintenance } from 'src/app/models/IAxeMaintenance';
import { ReperageGridLine } from 'src/app/models/IReperage';
import { ApiService } from 'src/app/services/api.service';
import { MapService } from 'src/app/services/map.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { IPointRepere } from 'src/app/models/IPointRepere';
import { DropDownService } from 'src/app/services/dropdown.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'saisie-reperage',
  templateUrl: './saisie-reperage.component.html',
  styleUrls: ['./saisie-reperage.component.less']
})
export class SaisieReperageComponent implements OnInit, OnDestroy {

  @Input() reperages: ReperageGridLine[];

  private subscriptions: Subscription[];
  fakeReperageId: number;

  deletedReperage: any[];

  hasWSError: boolean;
  wsErrorMessage: string;
  hasInputError: boolean;
  inputErrorRowIndex: number;

  cols: any[] = [
    { field: 'axe', header: 'Axe', type: 'string', show: true, width: '180px' },
    { field: 'debutPr', header: 'Début PR', type: 'string', show: true, width: '120px' },
    { field: 'distMaxDebut', header: 'Début Dist. max', type: 'string', show: true },
    { field: 'distanceDebut', header: 'Début distance', type: 'string', show: true },
    { field: 'finPr', header: 'Fin PR', type: 'string', show: true, width: '120px' },
    { field: 'distMaxFin', header: 'Fin Dist. max', type: 'string', show: true },
    { field: 'distanceFin', header: 'Fin distance', type: 'string', show: true },
    { field: 'action', header: 'Actions', type: 'action', filterable: false, show: true, export: false, width: '40px' }
  ];

  public opened = false;
  crudMode: string;

  axeMaintenances: IAxeMaintenance[];
  filteredAxeMaintenances: IAxeMaintenance[];

  constructor(private navigationService: NavigationService, private route: ActivatedRoute,
    private apiService: ApiService, private mapService: MapService) {
    this.crudMode = 'READ_ONLY';
    this.fakeReperageId = -1;
    this.subscriptions = [];
    this.axeMaintenances = [];
    this.reperages = [];
    this.deletedReperage = [];
    this.hasWSError = false;
    this.wsErrorMessage = null;
    this.hasInputError = false;
  }

  ngOnInit() {
    const editPath = this.route.snapshot.url.findIndex(url => url.path === 'edit');
    const viewPath = this.route.snapshot.url.findIndex(url => url.path === 'view');
    if (viewPath > -1) {
      this.crudMode = 'READ_ONLY';
    } else if (editPath > -1) {
      this.crudMode = 'EDIT';
    } else {
      this.crudMode = 'NEW';
    }
    this.setSubscriptions();
    this.deletedReperage = [];
    this.hasWSError = false;
    this.wsErrorMessage = null;
    this.hasInputError = false;
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  public close() {
    this.hasWSError = false;
    this.wsErrorMessage = null;
    this.hasInputError = false;
    if (this.crudMode === 'READ_ONLY') {
      this.opened = false;
    } else {
      if (this.checkValidReperages()) {
        this.hasInputError = true;
      } else {
        const newReperages = [];
        this.reperages.forEach(reperage => {
          if (!reperage.fromDb && !reperage.drawn) {
            newReperages.push(reperage);
          }
        });
        if (newReperages.length > 0) {
          this.apiService.getGeometryReperages(newReperages).subscribe(geometries => {
            if (geometries && Array.isArray(geometries)) {
              const geometriesReperages = [];
              geometries.forEach((geom, index) => {
                if (geom.error) {
                  this.hasWSError = true;
                  this.wsErrorMessage = geom.message;
                } else {
                  geometriesReperages.push(geom);
                }
              });
              if (!this.hasWSError) {
                this.mapService.updateFeatures(geometriesReperages, this.deletedReperage);
                this.reperages.map(rep => {
                  rep.drawn = true;
                });
                this.opened = false;
              }
            }
          });
        } else {
          this.mapService.updateFeatures([], this.deletedReperage);
          this.opened = false;
        }
      }
    }
  }

  public open() {
    this.deletedReperage = [];
    this.hasWSError = false;
    this.wsErrorMessage = null;
    this.hasInputError = false;
    this.opened = true;
  }

  checkValidReperages(): boolean {
    let error = false;
    this.reperages.forEach((reperage, index) => {
      if (!reperage.fromDb && !reperage.drawn) {
        if (!reperage.axe || !reperage.debutPr || !reperage.finPr) {
          error = true;
          this.inputErrorRowIndex = index + 1;
        }
      }
    });
    return error;
  }

  filterAxeMaintenances(event, rowIndex) {
    this.reperages[rowIndex].filteredAxeMaintenances = [];
    for (const axeMaintenance of this.axeMaintenances) {
      if (axeMaintenance.nom_complet.toLowerCase().includes(event.toLowerCase())) {
        this.reperages[rowIndex].filteredAxeMaintenances.push(axeMaintenance);
      }
    }
    /* this.prDebut.reset();
    this.prFin.reset(); */
  }

  onAxeMaintenanceChanged(event, rowIndex) {
    if (event) {
      this.reperages[rowIndex].axe = event;
      this.apiService.getPrByAxeMaintenance(this.reperages[rowIndex].axe)
        .subscribe(data => {
          this.reperages[rowIndex].prDebuts = [];
          this.reperages[rowIndex].filteredPrDebuts = [];
          const prDebuts: IPointRepere[] = [];
          const prFins: IPointRepere[] = [];
          data.forEach(val => {
            if (val.secteur_longueur > 0) {
              prDebuts.push(val);
            }
            prFins.push(val);
          });
          prDebuts.sort((a1, a2) => {
            return (Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence));
          });
          prFins.sort((a1, a2) => {
            return (Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence));
          });
          this.reperages[rowIndex].prDebuts = prDebuts;
          this.reperages[rowIndex].filteredPrDebuts = [...prDebuts];
          this.reperages[rowIndex].prFins = prFins;
          this.reperages[rowIndex].filteredPrFins = [...prFins];
        });
    } else {
      this.reperages[rowIndex].axe = null;
      this.reperages[rowIndex].debutPr = null;
      this.reperages[rowIndex].prDebuts = [];
      this.reperages[rowIndex].filteredPrDebuts = [];
      this.reperages[rowIndex].finPr = null;
      this.reperages[rowIndex].prFins = [];
      this.reperages[rowIndex].filteredPrFins = [];
    }
  }

  onDebutPrChanged(event, rowIndex) {
    if (event) {
      this.reperages[rowIndex].finPr = null;
      this.filterPrFins('', rowIndex);
    } else {
      this.reperages[rowIndex].finPr = null;
      this.reperages[rowIndex].filteredPrFins = this.reperages[rowIndex].prFins;
    }
    this.checkDebutDistance(rowIndex);
    this.checkFinDistance(rowIndex);
  }

  onFinPrChanged(event, rowIndex) {
    this.checkFinDistance(rowIndex);
  }

  checkDebutDistance(rowIndex: number) {
    if (!this.reperages[rowIndex].debutPr || this.reperages[rowIndex].distanceDebut > this.reperages[rowIndex].debutPr.secteur_longueur) {
      this.reperages[rowIndex].distanceDebut = null;
    }
  }

  checkFinDistance(rowIndex: number) {
    // If fin distance > fin dist.max reset value // If debut seq_sec == fin seq_sec && distanceFin > distanceDebut reset value
    if (this.reperages[rowIndex].finPr && this.reperages[rowIndex].distanceFin > this.reperages[rowIndex].finPr.secteur_longueur) {
      this.reperages[rowIndex].distanceFin = null;
    } else if (this.reperages[rowIndex].debutPr && this.reperages[rowIndex].finPr
      && this.reperages[rowIndex].debutPr.secteur_nom === this.reperages[rowIndex].finPr.secteur_nom
      && this.reperages[rowIndex].distanceFin < this.reperages[rowIndex].distanceDebut) {
      this.reperages[rowIndex].distanceFin = null;
    }
  }

  onBlurDebutDistanceEdition(rowIndex: number) {
    this.checkDebutDistance(rowIndex);
  }

  onBlurFinDistanceEdition(rowIndex: number) {
    this.checkFinDistance(rowIndex);
  }

  filterPrDebuts(event, rowIndex) {
    if (!this.reperages[rowIndex] && !this.reperages[rowIndex].axe) {
      return [];
    }

    this.reperages[rowIndex].filteredPrDebuts = [];
    for (const prDebut of this.reperages[rowIndex].prDebuts) {
      if (prDebut.secteur_nom.toLowerCase().includes(event.toLowerCase()) && prDebut.secteur_longueur > 0) {
        this.reperages[rowIndex].filteredPrDebuts.push(prDebut);
      }
    }
    this.reperages[rowIndex].filteredPrDebuts.sort((a1, a2) => {
      return (Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence));
    });
  }

  filterPrFins(event, rowIndex) {
    if (!this.reperages[rowIndex] && !this.reperages[rowIndex].axe) {
      return [];
    }

    this.reperages[rowIndex].filteredPrFins = [];
    for (const prFin of this.reperages[rowIndex].prFins) {
      if (prFin.secteur_nom.toLowerCase().includes(event.toLowerCase())) {
        const prDebut = this.reperages[rowIndex].debutPr;
        if (!prDebut || Number(prFin.segment_sequence) > Number(prDebut.segment_sequence) ||
          (Number(prFin.segment_sequence) === Number(prDebut.segment_sequence)
            && Number(prFin.secteur_sequence) >= Number(prDebut.secteur_sequence))) {
          this.reperages[rowIndex].filteredPrFins.push(prFin);
        }
      }
    }
    this.reperages[rowIndex].filteredPrFins.sort((a1, a2) => {
      return (Number(a1.segment_sequence) - Number(a2.segment_sequence) || Number(a1.secteur_sequence) - Number(a2.secteur_sequence));
    });
  }

  addReperage(): void {
    this.reperages.push(new ReperageGridLine({ id: this.fakeReperageId } as any, this.axeMaintenances));
    this.fakeReperageId = this.fakeReperageId - 1;
  }

  onDeleteReperageClick(rowIndex: number, reperage: ReperageGridLine): void {
    /* const index = this.reperages.findIndex(val => {
      return val.id === item.id;
    });
    if (index > -1) {
      this.reperages.splice(index, 1);
    } */

    this.deletedReperage.push(reperage.id);
    this.reperages.splice(rowIndex, 1);
  }

  deleteReperageById(reperageId): void {
    const repIndex = this.reperages.findIndex(rep => {
      return rep.id === reperageId;
    });
    if (repIndex > -1) {
      this.reperages.splice(repIndex, 1);
    }
  }

  private setSubscriptions(): void {
    this.subscriptions.push(
      this.navigationService.openSaisieReperageDialog$.subscribe(val => {
        this.open();
      })
    );

    this.subscriptions.push(
      this.apiService.getAxeMaintenances().subscribe(data => {
        data.sort((a1, a2) => {
          let a1Nom = '';
          let a2Nom = '';
          if (a1.nom_complet) {
            a1Nom = a1.nom_complet.toLowerCase();
          }
          if (a2.nom_complet) {
            a2Nom = a2.nom_complet.toLowerCase();
          }
          return a1Nom.localeCompare(a2Nom);
        });
        this.axeMaintenances = data;
        this.filteredAxeMaintenances = data;
      })
    );

    this.subscriptions.push(
      this.mapService.featureWithReperageIdRemoved$.subscribe((val: { id_reperage: number }) => {
        this.deleteReperageById(val.id_reperage);
      })
    );

    /*     this.axeMaintenance.valueChanges.subscribe(value => {
          this.filteredPrDebuts = [];
          this.filteredPrFins = [];
          if (value) {
            this.prDebut.enable();
            this.prFin.enable();
            this.apiService.getPrByAxeMaintenance(this.axeMaintenance.value)
              .subscribe(data => {
                this.prDebuts = data;
                this.filteredPrDebuts = data;
              });
            this.apiService.getPrByAxeMaintenance(this.axeMaintenance.value).subscribe(data => {
              this.prFins = data;
              this.filteredPrFins = data;
            });
          } else {
            this.prDebut.disable();
            this.prFin.disable();
          }
        }); */
  }

  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }



}

