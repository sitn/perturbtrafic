import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { LoaderService } from 'src/app/core/loader/loader.service';
import { IFormulairePerturbation } from 'src/app/models/perturbation/IFormulairePerturbation';
import { IPerturbationServerEdition } from 'src/app/models/perturbation/IPerturbation';
import { ApiService } from 'src/app/services/api.service';
import { ConfigService } from 'src/app/services/config.service';
import { DropDownService } from 'src/app/services/dropdown.service';
import { MapService } from 'src/app/services/map.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

import { AvisPerturbationComponent } from './avis-perturbation/avis-perturbation.component';
import { UserService } from 'src/app/services/user.service';

@Component({
    selector: 'formulaire-perturbation',
    templateUrl: './formulaire-perturbation.component.html',
    styleUrls: ['./formulaire-perturbation.component.less']
})
export class FormulairePerturbationComponent implements OnInit {

    @ViewChild('preavisComponent', { static: false })
    public preavisComponent: AvisPerturbationComponent;

    perturbation: IFormulairePerturbation;
    mode: string;

    mapImageForPDF: any;

    private subscriptions: Subscription[];

    get typeEvenement() { return (this.perturbationFormService.perturbationForm.controls.evenement as FormGroup).controls.type; }
    get typePerturbation() { return this.perturbationFormService.perturbationForm.controls.type; }

    constructor(private fb: FormBuilder, public perturbationFormService: PerturbationFormService, private ref: ChangeDetectorRef,
        private dropDownService: DropDownService, private route: ActivatedRoute, private apiService: ApiService,
        private loaderService: LoaderService, private router: Router, private mapService: MapService,
        private navigationService: NavigationService, private configService: ConfigService, private userService: UserService) {

        this.subscriptions = [];

        /* const nouvelEvenement: IEvenement = <IEvenement>{};
        nouvelEvenement.type = { id: '-', value: null };
        this.evenement = {
          mode: 'CREATE',
          evenement: nouvelEvenement
        }; */
    }

    private createForm(): FormGroup {
        return this.fb.group({
            division: new FormControl('', [
                Validators.required
            ])
        });
    }

    ngOnInit() {
        this.perturbationFormService.evenement.setValue(null);
        this.perturbationFormService.perturbationForm.enable();
        this.perturbationFormService.reset();
        this.perturbationFormService.mode = 'NEW';
        const perturbationId = this.route.snapshot.paramMap.get('id');
        if (this.userService.canEditPerturbationState()) {
            this.perturbationFormService.perturbationForm.controls.etat.enable();
        }
        if (perturbationId) {
            this.apiService.getFullPerturbationById(perturbationId).subscribe(res => {
                const editPath = this.route.snapshot.url.findIndex(url => url.path === 'edit');
                const viewPath = this.route.snapshot.url.findIndex(url => url.path === 'view');
                const clonePath = this.route.snapshot.url.findIndex(url => url.path === 'clone');
                this.perturbationFormService.patchValues(res, clonePath > -1);
                this.preavisComponent.setCheckedContacts(res.contacts_a_aviser, res.perturbation.type);
                if (viewPath > -1) {
                    this.perturbationFormService.mode = 'READ_ONLY';
                    this.perturbationFormService.perturbationForm.disable();
                    this.ref.detectChanges();
                } else if (editPath > -1) {
                    this.perturbationFormService.mode = 'EDIT';
                    this.perturbationFormService.perturbationForm.controls.evenement.disable();
                    this.perturbationFormService.typePerturbation.disable();
                } else if (clonePath > -1) {
                    this.perturbationFormService.mode = 'NEW';
                    this.perturbationFormService.perturbationForm.controls.evenement.disable();
                    this.perturbationFormService.typePerturbation.disable();
                } else {
                    this.perturbationFormService.mode = 'NEW';
                }
            });
        } else {
            if (history && history.state && history.state.evenementId) {
                this.setValuesFromEvenementSelection(history.state.evenementId);
                this.perturbationFormService.perturbationForm.controls.evenement.disable();
            }
        }

        this.dropDownService.getContacts();
        this.dropDownService.getOrganismes();
        this.dropDownService.getLocalitesNPA();
        this.dropDownService.getLibellesEvenements();
        this.setSubscriptions();
        // this.form = this.createForm();
    }

    onSaveEvent() {
        // Here we clear the validations for dateDebut and DateFin, because Kendo DatePicker min and max options is updated
        // from the UI but not for validations.
        this.perturbationFormService.dateDebut.clearValidators();
        this.perturbationFormService.dateDebut.updateValueAndValidity();
        this.perturbationFormService.dateFin.clearValidators();
        this.perturbationFormService.dateFin.updateValueAndValidity();
        if (this.perturbationFormService.mode === 'NEW') {
            this.saveNewPerturbation();
        } else if (this.perturbationFormService.mode === 'EDIT') {
            this.editPerturbation();
        }
    }


    saveNewPerturbation() {
        if (!this.perturbationFormService.perturbationForm.valid) {
            this.navigationService.openErrorDialog('Le formulaire n est pas valide', 'Formulaire invalide');
            this.perturbationFormService.markAsTouched();
            this.perturbationFormService.markAsDirty();
        } else {
            const features = this.mapService.prepareFeaturesForSaving(this.perturbationFormService.reperages);
            const deviations = this.mapService.prepareDeviationsFeaturesForSaving();
            if (!features || features.length < 1) {
                this.navigationService.openErrorDialog('Aucune géométrie saisie', 'Formulaire invalide');
                this.perturbationFormService.markAsTouched();
                this.perturbationFormService.markAsDirty();
            } else {
                const avisContact = this.preavisComponent.getCheckedContacts();
                this.apiService.savePerturbation(
                    this.perturbationFormService.perturbationForm.getRawValue(), this.userService.currentUser,
                    features, deviations, avisContact)
                    .subscribe(res => {
                        if (!res.error) {
                            this.navigationService.openErrorDialog(
                                `La perturbation a été enregistrée correctement`, 'Perturbation enregistrée');
                            this.router.navigate([`/perturbations`]);
                        } else {
                            this.navigationService.openErrorDialog(
                                `Une erreur est survenue lors de la sauvegarde : ${res.message}`, 'Erreur');
                        }
                    });
            }
        }
    }

    editPerturbation() {
        if (!this.perturbationFormService.perturbationForm.valid) {
            this.navigationService.openErrorDialog('Le formulaire n est pas valide', 'Formulaire invalide');
            this.perturbationFormService.markAsTouched();
            this.perturbationFormService.markAsDirty();
        } else {
            const features = this.mapService.prepareFeaturesForSaving(this.perturbationFormService.reperages);
            const deviations = this.mapService.prepareDeviationsFeaturesForSaving();
            if (!features || features.length < 1) {
                this.navigationService.openErrorDialog('Aucune géométrie saisie', 'Formulaire invalide');
                this.perturbationFormService.markAsTouched();
                this.perturbationFormService.markAsDirty();
            } else {
                const avisContact = this.preavisComponent.getCheckedContacts();
                this.apiService.editPerturbation(
                    this.perturbationFormService.perturbationForm.getRawValue(), features, deviations, avisContact).subscribe(res => {
                        if (!res.error) {
                            this.router.navigate([`/perturbations`]);
                            this.navigationService.openErrorDialog(
                                `La perturbation a été enregistrée correctement`, 'Perturbation enregistrée');
                        } else {
                            this.navigationService.openErrorDialog(
                                `Une erreur est survenue lors de la sauvegarde : ${res.message}`, 'Erreur');
                        }
                    });
            }
        }
    }

    printPerturbation() {

        window.open(
            `${window.location.origin}/perturbations/formulaire/print/${this.perturbationFormService.perturbationForm.controls.id.value}`,
            '_blank'
        );
    }

    setValuesFromEvenementSelection(evenementId: number) {
        this.apiService.getFullEvenementById(evenementId).subscribe(eve => {
            const perturbation = <IPerturbationServerEdition>{};
            perturbation.perturbation = {} as any;
            perturbation.perturbation.type = this.perturbationFormService.typePerturbation.value;
            perturbation.perturbation.id_evenement = eve.evenement.id;
            if (eve.reperages) {
                perturbation.reperages = eve.reperages;
            }
            perturbation.geometries = eve.geometries.filter(geom => {
                let geometry;
                try {
                    geometry = JSON.parse(geom.geometry);
                } catch (error) {

                }
                return geometry && geometry.type !== 'Polygon';
            });
            perturbation.deviations = eve.deviations;
            const mappings = this.configService.getFieldsMapping();
            for (const k in mappings) {
                if (eve.evenement[k]) {
                    perturbation.perturbation[mappings[k]] = eve.evenement[k];
                }
            }
            this.perturbationFormService.patchValues(perturbation);
        });
    }

    private setSubscriptions(): void {
        this.subscriptions.push(
            this.perturbationFormService.typePerturbation.valueChanges.subscribe(val => {
                this.mapService.setDeviation(val === 1);
            })
        );

        this.subscriptions.push(
            this.perturbationFormService.evenement.valueChanges.subscribe(val => {
                if (val && this.perturbationFormService.mode === 'NEW') {
                    this.setValuesFromEvenementSelection(val);
                }
            })
        );
    }
}
