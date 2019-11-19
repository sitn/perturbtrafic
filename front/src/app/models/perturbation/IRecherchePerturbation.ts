import { FormControl, FormGroup } from '@angular/forms';
import { DateUtils } from 'src/app/utils/date.utils';
import { IPointRepere } from '../IPointRepere';

export interface IRecherchePerturbation {
    type: string;
    axeMaintenance: string;
    etat: string;
    valide: string;
    prDebut: string;
    prFin: string;
    urgence: boolean;
    description: string;
    numeroDossier: string;
    typeEvenement: string;
    dateDebut: Date;
    dateFin: Date;
    compteurTouche: boolean;
    ajoutePar: string;
}


export class RecherchePerturbation {
    type: string;
    etat: string;
    urgence: string;
    axe: string;
    prDebutSegSeq: number;
    prDebutSecSeq: number;
    prFinSegSeq: number;
    prFinSecSeq: number;
    description: string;
    valide: string;
    numeroDossierEvenement: string;
    typeEvenement: number;
    dateDebut: string;
    dateFin: string;
    compteurTouche: string;
    ajoutePar: string;

    constructor(recherchePerturbationFormValues: any) {
        this.type = recherchePerturbationFormValues.type;
        this.etat = recherchePerturbationFormValues.etat;
        if (recherchePerturbationFormValues.urgence) {
            if (recherchePerturbationFormValues.urgence === 'no') {
                this.urgence = 'false';
            } else if (recherchePerturbationFormValues.urgence === 'yes') {
                this.urgence = 'true';
            }
        }
        if (recherchePerturbationFormValues.compteurTouche) {
            if (recherchePerturbationFormValues.compteurTouche === 'no') {
                this.compteurTouche = 'false';
            } else if (recherchePerturbationFormValues.compteurTouche === 'yes') {
                this.compteurTouche = 'true';
            }
        }
        if (recherchePerturbationFormValues.prDebut) {
            this.prDebutSegSeq = (recherchePerturbationFormValues.prDebut as IPointRepere).segment_sequence;
            this.prDebutSecSeq = (recherchePerturbationFormValues.prDebut as IPointRepere).secteur_sequence;
        }
        if (recherchePerturbationFormValues.prFin) {
            this.prFinSegSeq = (recherchePerturbationFormValues.prFin as IPointRepere).segment_sequence;
            this.prFinSecSeq = (recherchePerturbationFormValues.prFin as IPointRepere).secteur_sequence;
        }
        this.description = recherchePerturbationFormValues.description;
        this.valide = recherchePerturbationFormValues.valide;
        this.numeroDossierEvenement = recherchePerturbationFormValues.numeroDossier;
        this.typeEvenement = recherchePerturbationFormValues.typeEvenement;
        this.axe = recherchePerturbationFormValues.axeMaintenance ? recherchePerturbationFormValues.axeMaintenance.nom_complet : null;
        if (recherchePerturbationFormValues.dates && recherchePerturbationFormValues.dates.dateDebut) {
            this.dateDebut = DateUtils.formatDate(recherchePerturbationFormValues.dates.dateDebut);
        }
        if (recherchePerturbationFormValues.dates && recherchePerturbationFormValues.dates.dateFin) {
            this.dateFin = DateUtils.formatDate(recherchePerturbationFormValues.dates.dateFin);
        }
        if (recherchePerturbationFormValues.ajoutePar) {
            this.ajoutePar = recherchePerturbationFormValues.ajoutePar.id;
        }
    }
}


export class RecherchePerturbationForm {
    type = new FormControl();
    axeMaintenance = new FormControl();
    etat = new FormControl();
    urgence = new FormControl('unknown');
    prDebut = new FormControl();
    prFin = new FormControl();
    description = new FormControl();
    valide = new FormControl();
    numeroDossier = new FormControl();
    typeEvenement = new FormControl();
    dates = new FormGroup({
        dateDebut: new FormControl(),
        dateFin: new FormControl()
    }, this.dateOrderValidator);
    compteurTouche = new FormControl('unknown');
    ajoutePar = new FormControl();


    private dateOrderValidator(g: FormGroup) {
        const valueDebut = g.get('dateDebut').value;
        const valueFin: any = g.get('dateFin');
        const valueFinValue = g.get('dateFin').value;

        if (valueDebut && valueFinValue) {
            const debut = new Date(valueDebut);
            const fin = new Date(valueFinValue);

            if (debut > fin) {
                valueFin.setErrors({ 'invalid: ': true });
                return { 'invalidDates': { value: 'pb dates' } };
            } else {
                return null;
            }
        }

        return null;
    }
}

