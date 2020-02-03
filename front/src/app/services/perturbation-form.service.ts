import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

import { IContact } from '../models/IContact';
import { ReperageGridLine } from '../models/IReperage';
import { IPerturbationServerEdition, PerturbationForm, PerturbationFormValues } from '../models/perturbation/IPerturbation';
import { ApiService } from './api.service';
import { MapService } from './map.service';
import { DropDownService } from './dropdown.service';

@Injectable()
export class PerturbationFormService {
    perturbationForm: FormGroup = this.fb.group(
        new PerturbationForm()
    );

    mode: string;
    geometries: any[];
    deviations: any[];
    reperages: any;
    avisContacts: IContact[];

    etatsLOV: { name: string, code: number }[];

    constructor(private fb: FormBuilder, private mapService: MapService, private apiService: ApiService,
        private dropDownService: DropDownService) {
        this.geometries = [];
        this.reperages = [];
        this.avisContacts = [];
        this.mode = 'READ_ONLY';
        this.etatsLOV = [];
        this.apiService.getEtats().subscribe(etats => {
            this.etatsLOV = etats;
        });
    }

    patchValues(perturbationServer: IPerturbationServerEdition, cloned = false) {
        this.geometries = [];
        this.reperages = [];
        this.deviations = [];
        this.avisContacts = [];
        this.geometries = perturbationServer.geometries;
        this.deviations = perturbationServer.deviations;
        if (perturbationServer.reperages) {
            perturbationServer.reperages.forEach(async reperage => {
                this.geometries.map(geom => {
                    const parsedGeom: any = JSON.parse(geom.geometry);
                    if ((['geometrycollection', 'linestring', 'multilinestring'].indexOf(parsedGeom.type.toLowerCase()) > -1)
                        && geom.id === reperage.id_perturbation_ligne) {
                        geom.id_reperage = reperage.id;
                    }
                });

                const wsReperage =
                    await this.apiService.getPrByAxeMaintenance({
                        nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                        proprietaire: reperage.proprietaire
                    }).toPromise();

                const wsPrDebut = wsReperage.find(pr => {
                    return pr.secteur_nom === reperage.pr_debut;
                });
                const wsPrFin = wsReperage.find(pr => {
                    return pr.secteur_nom === reperage.pr_fin;
                });

                const reperageGridLine = <ReperageGridLine>{};
                reperageGridLine.id = reperage.id;
                reperageGridLine.fromDb = true;
                reperageGridLine.axe = {
                    nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                    proprietaire: reperage.proprietaire
                };
                reperageGridLine.filteredAxeMaintenances = [{
                    nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                    proprietaire: reperage.proprietaire
                }];
                reperageGridLine.filteredPrDebuts = [
                    {
                        axe_nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                        secteur_nom: reperage.pr_debut,
                        secteur_longueur: null,
                        segment_sequence: null
                    }
                ];
                reperageGridLine.filteredPrFins = [
                    {
                        axe_nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                        secteur_nom: reperage.pr_fin,
                        secteur_longueur: null,
                        segment_sequence: null
                    }
                ];
                reperageGridLine.debutPr = {
                    axe_nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                    secteur_nom: reperage.pr_debut,
                    secteur_longueur: wsPrDebut ? wsPrDebut.secteur_longueur : null,
                    segment_sequence: null
                };
                reperageGridLine.finPr = {
                    axe_nom_complet: [reperage.proprietaire, reperage.axe, reperage.sens].join(':'),
                    secteur_nom: reperage.pr_fin,
                    secteur_longueur: wsPrFin ? wsPrFin.secteur_longueur : null,
                    segment_sequence: null
                };
                reperageGridLine.distanceDebut = reperage.pr_debut_distance;
                reperageGridLine.distanceFin = reperage.pr_fin_distance;
                this.reperages.push(reperageGridLine);
            });
        }
        this.avisContacts = perturbationServer.contacts_a_aviser;
        const patched = new PerturbationFormValues(perturbationServer, cloned);
        this.mapService.initializeFeaturesAndExtent(this.geometries);
        this.mapService.initializeDeviationsAndExtent(this.deviations);
        this.perturbationForm.patchValue(patched, { emitEvent: false });
    }

    reset() {
        this.geometries = [];
        this.reperages = [];
        this.avisContacts = [];
        this.perturbationForm.controls.etat.disable();
        this.perturbationForm.controls.urgence.disable();
        this.perturbationForm.controls.utilisateurValidation.disable();
        this.perturbationForm.controls.dateValidation.disable();
        this.perturbationForm.controls.utilisateurAjout.disable();
        this.perturbationForm.controls.dateAjout.disable();
        this.perturbationForm.controls.utilisateurModification.disable();
        this.perturbationForm.controls.dateModification.disable();
        this.perturbationForm.reset();
        // this.disableGeneralInfos();
    }

    disableGeneralInfos() {
        this.perturbationForm.controls.dates.disable();
        this.perturbationForm.controls.description.disable();
        this.perturbationForm.controls.localisation.disable();
        this.perturbationForm.controls.trancheHoraire.disable();
        this.perturbationForm.controls.responsableTrafic.disable();
        this.perturbationForm.controls.remarque.disable();
        this.perturbationForm.controls.urgence.disable();
        this.perturbationForm.controls.etat.disable();
        this.perturbationForm.controls.utilisateurValidation.disable();
        this.perturbationForm.controls.dateValidation.disable();
        this.perturbationForm.controls.dateDecision.disable();
        this.perturbationForm.controls.decision.disable();
    }

    enableGeneralInfos() {
        this.perturbationForm.controls.dates.enable();
        this.perturbationForm.controls.description.enable();
        this.perturbationForm.controls.localisation.enable();
        this.perturbationForm.controls.trancheHoraire.enable();
        this.perturbationForm.controls.responsableTrafic.enable();
        this.perturbationForm.controls.remarque.enable();
        this.perturbationForm.controls.urgence.enable();
        this.perturbationForm.controls.etat.enable();
        this.perturbationForm.controls.utilisateurValidation.enable();
        this.perturbationForm.controls.dateValidation.enable();
        this.perturbationForm.controls.dateDecision.enable();
        this.perturbationForm.controls.decision.enable();
    }

    markAsDirty() {
        this.markFormGroupDirty(this.perturbationForm);
    }

    markFormGroupDirty = (formGroup) => {
        (<any>Object).values(formGroup.controls).forEach(control => {
            control.markAsDirty();

            if (control.controls) {
                this.markFormGroupDirty(control);
            }
        });
    }

    markAsTouched() {
        this.markFormGroupTouched(this.perturbationForm);
    }

    markFormGroupTouched = (formGroup) => {
        (<any>Object).values(formGroup.controls).forEach(control => {
            control.markAsTouched();

            if (control.controls) {
                this.markFormGroupTouched(control);
            }
        });
    }

    /*
    *** Infos générales
    */

    get dates() { return (this.perturbationForm.controls.dates as FormGroup); }
    get dateDebut() { return this.dates.controls.dateDebut; }
    get dateFin() { return this.dates.controls.dateFin; }

    get typePerturbation() { return this.perturbationForm.controls.type; }

    get typeOccupation() { return (this.perturbationForm.controls.occupation as FormGroup).controls.typeOccupation; }

    get evenement() {
        return (this.perturbationForm.controls.evenement as FormGroup).controls.evenement;
    }

    get responsableTraficContactInfos() {
        return (this.perturbationForm.controls.responsableTrafic as FormGroup).controls.contactInfos as FormGroup;
    }
    get responsableTraficId() {
        return (this.perturbationForm.controls.responsableTrafic as FormGroup).controls.contact;
    }

    /*
*** Fermeture
*/
    get responsableFermeture() {
        return (this.perturbationForm.controls.fermeture as FormGroup).controls.responsable;
    }

    /*
*** Occupation
*/
    get responsableOccupation() {
        return (this.perturbationForm.controls.occupation as FormGroup).controls.responsable;
    }

    getEtatLabel(etatId: number): string {
        let etatLabel;
        const etat = this.etatsLOV.find(val => {
            return val.code === etatId;
        });
        if (etat) {
            etatLabel = etat.name;
        }
        return etatLabel;
    }
}
