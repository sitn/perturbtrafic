import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

import { IEvenementServerEdition } from '../models/evenement/IEvenement';
import { EvenementForm, EvenementFormValues } from '../models/evenement/IEvenementForm';
import { ReperageGridLine } from '../models/IReperage';
import { MapService } from './map.service';
import { ApiService } from './api.service';

@Injectable()
export class EvenementFormService {

    evenementForm: FormGroup = this.fb.group(
        new EvenementForm()
    );

    mode: string;
    geometries: any;
    reperages: ReperageGridLine[];

    constructor(private fb: FormBuilder, private mapService: MapService, private apiService: ApiService) {
        this.geometries = [];
        this.reperages = [];
        this.mode = 'READ_ONLY';
    }

    patchValues(evenementServer: IEvenementServerEdition) {
        this.reperages = [];
        this.geometries = evenementServer.geometries;
        if (evenementServer.reperages) {
            evenementServer.reperages.forEach(async reperage => {
                this.geometries.map(geom => {
                    const parsedGeom: any = JSON.parse(geom.geometry);
                    if ((['geometrycollection', 'linestring', 'multilinestring'].indexOf(parsedGeom.type.toLowerCase()) > -1)
                        && geom.id === reperage.id_evenement_ligne) {
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
                reperageGridLine.fromDb = true;
                reperageGridLine.id = reperage.id;
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
        const patched = new EvenementFormValues(evenementServer);
        this.mapService.initializeFeaturesAndExtent(this.geometries);
        this.evenementForm.patchValue(patched);
    }

    reset() {
        this.geometries = [];
        this.reperages = [];
        this.evenementForm.reset();
        this.evenementForm.controls.dateDemande.setValue(new Date());
        this.dateDebut.setValue(null);
        this.dateFin.setValue(null);
        this.evenementForm.controls.numeroDossier.disable();
        this.evenementForm.controls.utilisateurAjout.disable();
        this.evenementForm.controls.dateAjout.disable();
        this.evenementForm.controls.utilisateurModification.disable();
        this.evenementForm.controls.dateModification.disable();
        this.resetChantierValues();
        this.resetFouilleValues();
    }

    resetChantierValues() {
        this.chantierBoucleInduction.setValue(false);
        this.chantierFaucherAccotement.setValue(false);
        this.chantierCurerDepotoirs.setValue(false);
        this.chantierNettoyerBords.setValue(false);
        this.chantierColmaterFissure.setValue(false);
        this.chantierPrTouches.setValue(false);
        this.chantierReperageEffectif.setValue(false);
    }

    resetFouilleValues() {
        this.fouillePrTouches.setValue(false);
        this.fouilleReperageEffectif.setValue(false);
    }

    markAsDirty() {
        this.markFormGroupDirty(this.evenementForm);
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
        this.markFormGroupTouched(this.evenementForm);
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
    *** Controles infos générales
    */
    get numeroDossier() { return this.evenementForm.controls.numeroDossier; }
    get libelle() { return this.evenementForm.controls.libelle; }
    get dates() { return (this.evenementForm.controls.dates as FormGroup); }
    get dateDebut() { return this.dates.controls.dateDebut; }
    get dateFin() { return this.dates.controls.dateFin; }
    get typeEvenement() { return (this.evenementForm.controls.type as FormGroup).controls.type; }

    get requerantId() {
        return (this.evenementForm.controls.requerant as FormGroup).controls.organisme;
    }
    get requerantContactInfos() {
        return (this.evenementForm.controls.requerant as FormGroup).controls.contactInfos as FormGroup;
    }
    get personneContactId() {
        return (this.evenementForm.controls.contact as FormGroup).controls.contact;
    }
    get personneContactInfos() {
        return (this.evenementForm.controls.contact as FormGroup).controls.contactInfos as FormGroup;
    }

    /*
    *** Controles Autre
    */

    get autreFormGroup(): FormGroup {
        return (this.evenementForm.controls.autre as FormGroup);
    }

    get autreMaitreOuvrageId() {
        return (this.autreFormGroup.controls.maitreOuvrage as FormGroup).controls.organisme;
    }
    get autreMaitreOuvrageContactInfos() {
        return (this.autreFormGroup.controls.maitreOuvrage as FormGroup).controls.contactInfos as FormGroup;
    }

    get autreDirectionLocaleId() {
        return (this.autreFormGroup.controls.directionLocale as FormGroup).controls.contact;
    }
    get autreDirectionLocaleContactInfos() {
        return (this.autreFormGroup.controls.directionLocale as FormGroup).controls.contactInfos as FormGroup;
    }

    get autreEntrepreneurId() {
        return (this.autreFormGroup.controls.entrepreneur as FormGroup).controls.organisme;
    }
    get autreEntrepreneurContactInfos() {
        return (this.autreFormGroup.controls.entrepreneur as FormGroup).controls.contactInfos as FormGroup;
    }

    get autreResponsableTravauxId() {
        return (this.autreFormGroup.controls.responsableTravaux as FormGroup).controls.contact;
    }
    get autreResponsableTravauxContactInfos() {
        return (this.autreFormGroup.controls.responsableTravaux as FormGroup).controls.contactInfos as FormGroup;
    }

    /*
    *** Controles Chantier
    */


    get chantierFormGroup(): FormGroup {
        return (this.evenementForm.controls.chantier as FormGroup);
    }
    get directionLocale() {
        return (this.chantierFormGroup.controls.directionLocale);
    }
    get responsableTravaux() {
        return (this.chantierFormGroup.controls.responsableTravaux);
    }
    get maitreOuvrage() {
        return (this.chantierFormGroup.controls.maitreOuvrage);
    }
    get entrepreneur() {
        return (this.chantierFormGroup.controls.entrepreneur);
    }
    get chantierBoucleInduction() {
        return this.chantierFormGroup.controls.boucleInduction;
    }
    get chantierFaucherAccotement() {
        return this.chantierFormGroup.controls.faucherAccotement;
    }
    get chantierCurerDepotoirs() {
        return this.chantierFormGroup.controls.curerDepotoirs;
    }
    get chantierNettoyerBords() {
        return this.chantierFormGroup.controls.nettoyerBords;
    }
    get chantierColmaterFissure() {
        return this.chantierFormGroup.controls.colmaterFissure;
    }
    get chantierPrTouches() {
        return this.chantierFormGroup.controls.prTouches;
    }
    get chantierReperageEffectif() {
        return this.chantierFormGroup.controls.reperageEffectif;
    }

    /*
    *** Controles Fouille
    */

    get fouilleFormGroup(): FormGroup { return this.evenementForm.controls.fouille as FormGroup; }

    get fouillePrTouches() {
        return this.fouilleFormGroup.controls.prTouches;
    }
    get fouilleReperageEffectif() {
        return this.fouilleFormGroup.controls.reperageEffectif;
    }

    get fouilleDirectionLocaleId() {
        return (this.fouilleFormGroup.controls.directionLocale as FormGroup).controls.contact;
    }
    get fouilleDirectionLocaleContactInfos() {
        return (this.fouilleFormGroup.controls.directionLocale as FormGroup).controls.contactInfos as FormGroup;
    }
    get fouilleMaitreOuvrageId() {
        return (this.fouilleFormGroup.controls.maitreOuvrage as FormGroup).controls.organisme;
    }
    get fouilleMaitreOuvrageContactInfos() {
        return (this.fouilleFormGroup.controls.maitreOuvrage as FormGroup).controls.contactInfos as FormGroup;
    }
    get fouilleEntrepreneurId() {
        return (this.fouilleFormGroup.controls.entrepreneur as FormGroup).controls.organisme;
    }
    get fouilleEntrepreneurContactInfos() {
        return (this.fouilleFormGroup.controls.entrepreneur as FormGroup).controls.contactInfos as FormGroup;
    }
    get fouilleResponsableTravauxId() {
        return (this.fouilleFormGroup.controls.responsableTravaux as FormGroup).controls.contact;
    }
    get fouilleResponsableTravauxContactInfos() {
        return (this.fouilleFormGroup.controls.responsableTravaux as FormGroup).controls.contactInfos as FormGroup;
    }
}
