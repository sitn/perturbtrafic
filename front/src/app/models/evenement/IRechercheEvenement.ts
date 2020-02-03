import { FormControl, FormGroup } from '@angular/forms';
import { IPointRepere } from '../IPointRepere';

export interface IRechercheEvenement {
    numeroDossier: string;
    type: string;
    prevision: boolean;
    libelle: string;
    dateDebut: Date;
    dateFin: Date;
    division: string;
    nomRequerant: number;
    idResponsable: number;
    axeMaintenance: string;
    prDebut: string;
    prFin: string;
    ajoutePar: string;
    srbTouche: boolean;
    compteurTouche: boolean;
}

export class RechercheEvenement {
    numeroDossier: string;
    type: number;
    prevision: string;
    libelle: string;
    dateDebut: string;
    dateFin: string;
    division: string;
    nomRequerant: number;
    idResponsable: number;
    axe: string;
    prDebutSegSeq: number;
    prDebutSecSeq: number;
    prFinSegSeq: number;
    prFinSecSeq: number;
    ajoutePar: string;
    prTouche: string;
    compteurTouche: string;
    localite: string;

    constructor(rechercheEvenementForm: any) {
        this.numeroDossier = rechercheEvenementForm.numeroDossier;
        this.type = rechercheEvenementForm.type;
        if (rechercheEvenementForm.prevision) {
            if (rechercheEvenementForm.prevision === 'no') {
                this.prevision = 'false';
            } else if (rechercheEvenementForm.prevision === 'yes') {
                this.prevision = 'true';
            }
        }
        if (rechercheEvenementForm.compteurTouche) {
            if (rechercheEvenementForm.compteurTouche === 'no') {
                this.compteurTouche = 'false';
            } else if (rechercheEvenementForm.compteurTouche === 'yes') {
                this.compteurTouche = 'true';
            }
        }
        if (rechercheEvenementForm.srbTouche) {
            if (rechercheEvenementForm.srbTouche === 'no') {
                this.prTouche = 'false';
            } else if (rechercheEvenementForm.srbTouche === 'yes') {
                this.prTouche = 'true';
            }
        }
        this.libelle = rechercheEvenementForm.libelle;
        if (rechercheEvenementForm.dates && rechercheEvenementForm.dates.dateDebut) {
            this.dateDebut = formatDate(rechercheEvenementForm.dates.dateDebut);
        }
        if (rechercheEvenementForm.dates && rechercheEvenementForm.dates.dateFin) {
            this.dateFin = formatDate(rechercheEvenementForm.dates.dateFin);
        }
        this.division = rechercheEvenementForm.division;
        this.nomRequerant = rechercheEvenementForm.requerant;
        this.idResponsable = rechercheEvenementForm.responsable;
        this.axe = rechercheEvenementForm.axeMaintenance ? rechercheEvenementForm.axeMaintenance.nom_complet : null;
        if (rechercheEvenementForm.prDebut) {
            this.prDebutSegSeq = (rechercheEvenementForm.prDebut as IPointRepere).segment_sequence;
            this.prDebutSecSeq = (rechercheEvenementForm.prDebut as IPointRepere).secteur_sequence;
        }
        if (rechercheEvenementForm.prFin) {
            this.prFinSegSeq = (rechercheEvenementForm.prFin as IPointRepere).segment_sequence;
            this.prFinSecSeq = (rechercheEvenementForm.prFin as IPointRepere).secteur_sequence;
        }
        if (rechercheEvenementForm.ajoutePar) {
            this.ajoutePar = rechercheEvenementForm.ajoutePar.id;
        }
    }
}


export class RechercheEvenementForm {
    numeroDossier = new FormControl();
    type = new FormControl();
    requerant = new FormControl();
    prevision = new FormControl('unknown');
    libelle = new FormControl();
    dates = new FormGroup({
        dateDebut: new FormControl(),
        dateFin: new FormControl(),
    }, this.dateOrderValidator);
    division = new FormControl();
    responsable = new FormControl();
    axeMaintenance = new FormControl();
    prDebut = new FormControl({ value: null, disabled: true });
    prFin = new FormControl({ value: null, disabled: true });
    ajoutePar = new FormControl();
    srbTouche = new FormControl('unknown');
    compteurTouche = new FormControl('unknown');

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

function formatDate(date) {
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();

    if (month.length < 2) {
        month = '0' + month;
    }
    if (day.length < 2) {
        day = '0' + day;
    }
    return [year, month, day].join('-');
}
