import { ChangeDetectorRef, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PDFExportComponent } from '@progress/kendo-angular-pdf-export';
import { Subscription } from 'rxjs';
import { LoaderService } from 'src/app/core/loader/loader.service';
import { Conflit } from 'src/app/models/IConflit';
import { IPerturbationImpression } from 'src/app/models/perturbation/IPerturbation';
import { ApiService } from 'src/app/services/api.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { MapService } from 'src/app/services/map.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'formulaire-evenement',
  templateUrl: './formulaire-evenement.component.html',
  styleUrls: ['./formulaire-evenement.component.less']
})
export class FormulaireEvenementComponent implements OnInit, OnDestroy {

  @ViewChild('pdfFolder', { static: false }) pdfFolder: PDFExportComponent;

  mode: string;

  newPerturbationDialogOpened: boolean;
  conflictPerturbationDialogOpened: boolean;
  conflictsLength: number;
  newEvenementCreatedId: number;

  mapImageForPDF: any;

  evenementPerturbationsImpression: IPerturbationImpression[];

  private subscriptions: Subscription[];

  get typeEvenement() { return (this.evenementFormService.evenementForm.controls.type as FormGroup).controls.type; }

  constructor(private fb: FormBuilder, public evenementFormService: EvenementFormService, private apiService: ApiService,
    private ref: ChangeDetectorRef, private dropDownService: DropDownService, private router: Router, private loaderService: LoaderService,
    private route: ActivatedRoute, private mapService: MapService, private navigationService: NavigationService,
    private userService: UserService) {
    this.subscriptions = [];
    this.newPerturbationDialogOpened = false;
    this.conflictPerturbationDialogOpened = false;
    this.mapImageForPDF = null;
    this.conflictsLength = 0;
    this.evenementPerturbationsImpression = [];
  }

  ngOnInit() {
    this.newPerturbationDialogOpened = false;
    this.newEvenementCreatedId = null;
    this.evenementFormService.evenementForm.enable();
    this.evenementFormService.reset();
    this.evenementFormService.mode = 'NEW';
    this.conflictsLength = 0;
    const evenementId = this.route.snapshot.paramMap.get('id');
    if (evenementId) {
      this.apiService.getFullEvenementById(evenementId).subscribe(res => {
        this.evenementFormService.patchValues(res);
        const editPath = this.route.snapshot.url.findIndex(url => url.path === 'edit');
        const viewPath = this.route.snapshot.url.findIndex(url => url.path === 'view');
        if (viewPath > -1) {
          this.evenementFormService.mode = 'READ_ONLY';
          this.evenementFormService.evenementForm.disable();
        } else if (editPath > -1) {
          this.evenementFormService.mode = 'EDIT';
          this.evenementFormService.evenementForm.controls.type.disable();
        }
        this.ref.detectChanges();
      });
    } else {
      this.evenementFormService.mode = 'NEW';
    }
    this.dropDownService.getContacts();
    this.dropDownService.getDivisions();
    this.dropDownService.getOrganismes();
    this.dropDownService.getLocalitesNPA();
    this.dropDownService.getCommunes();
    this.dropDownService.getDestinatairesFacturations();
    this.setSubscriptions();
    /* if (this.typeEvenement) {
      this.evenementFormService.typeEvenement.valueChanges.subscribe(value => {
        this.ref.detectChanges();
      });
    } */
  }

  ngOnDestroy() {
    this.cleanUpSubscriptions();
  }

  onSaveEvent() {

    // Here we clear the validations for dateDebut and DateFin, because Kendo DatePicker min and max options is updated 
    // from the UI but not for validations.
    this.evenementFormService.dateDebut.clearValidators();
    this.evenementFormService.dateDebut.updateValueAndValidity();
    this.evenementFormService.dateFin.clearValidators();
    this.evenementFormService.dateFin.updateValueAndValidity();
    if (this.evenementFormService.mode === 'NEW') {
      this.saveNewEvenement();
    } else if (this.evenementFormService.mode === 'EDIT') {
      this.editEvenement();
    }
  }

  printFolder() {
    window.open(`${window.location.origin}/evenements/formulaire/print_folder/${this.evenementFormService.evenementForm.controls.id.value}`,
      '_blank');
  }

  saveNewEvenement() {
    if (!this.evenementFormService.evenementForm.valid) {
      this.navigationService.openErrorDialog('Le formulaire n est pas valide', 'Formulaire invalide');
      this.evenementFormService.markAsTouched();
      this.evenementFormService.markAsDirty();
    } else {
      const features = this.mapService.prepareFeaturesForSaving(this.evenementFormService.reperages);
      if (!features || features.length < 1) {
        this.navigationService.openErrorDialog('Aucune géométrie saisie', 'Formulaire invalide');
        this.evenementFormService.markAsTouched();
        this.evenementFormService.markAsDirty();
      } else {
        this.apiService.saveEvenement(this.evenementFormService.evenementForm.getRawValue(), this.userService.currentUser, features)
          .subscribe(res => {
            if (!res.error) {
              if (res.id) {
                this.newEvenementCreatedId = res.id;
                this.newPerturbationDialogOpened = true;
              }
            } else {
              this.navigationService.openErrorDialog(`Une erreur est survenue lors de la sauvegarde : ${res.message}`, 'Erreur');
            }
          });
      }
    }
  }


  printEvenement() {
    window.open(`${window.location.origin}/evenements/formulaire/print/${this.evenementFormService.evenementForm.controls.id.value}`,
      '_blank');
  }


  editEvenement() {

    if (!this.evenementFormService.evenementForm.valid) {
      this.navigationService.openErrorDialog('Le formulaire n est pas valide', 'Formulaire invalide');
      this.evenementFormService.markAsTouched();
      this.evenementFormService.markAsDirty();
    } else {
      const features = this.mapService.prepareFeaturesForSaving(this.evenementFormService.reperages);
      if (!features || features.length < 1) {
        this.navigationService.openErrorDialog('Aucune géométrie saisie', 'Formulaire invalide');
        this.evenementFormService.markAsTouched();
        this.evenementFormService.markAsDirty();
      } else {
        this.apiService.editEvenement(this.evenementFormService.evenementForm.getRawValue(), this.userService.currentUser, features)
          .subscribe(res => {
            if (!res.error) {
              this.apiService.getConflitsByEvenementId(this.evenementFormService.evenementForm.get('id').value)
                .subscribe((conf: Conflit[]) => {
                  if (conf) {
                    this.conflictsLength = conf.length;
                  }
                  this.conflictPerturbationDialogOpened = true;
                });
            } else {
              this.navigationService.openErrorDialog(`Une erreur est survenue lors de la sauvegarde : ${res.message}`, 'Erreur');
            }
          });
      }
    }
  }

  showConflictsSection(el: HTMLElement) {
    this.conflictPerturbationDialogOpened = false;
    el.scrollIntoView();
  }

  routeToPerturbationFormulaire() {
    this.router.navigate(['/perturbations/formulaire'], { state: { evenementId: this.newEvenementCreatedId } });
  }

  routeToEvenementsListe() {
    this.router.navigate([`/evenements`]);
  }

  private setSubscriptions(): void {

  }

  private cleanUpSubscriptions(): void {
    let subscription: Subscription = null;

    while (subscription = this.subscriptions.pop()) {
      subscription.unsubscribe();
    }
  }


}
