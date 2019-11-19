import { IAxeMaintenance } from './IAxeMaintenance';
import { IPointRepere } from './IPointRepere';

export interface IReperage {
    id?: number;
    axe: IAxeMaintenance;
    debutPr: IPointRepere;
    distMaxDebut: number;
    distanceDebut: number;
    finPr: IPointRepere;
    distMaxFin: number;
    distanceFin: number;
}

export interface IReperageServer {
    type: number;
    f_surf?: any;
    ecartf: number;
    pr_fin_distance: number;
    pr_debut_distance: number;
    pr_debut: string;
    axe: any;
    id_deviation: number;
    id_evenement_ligne?: number;
    id: any;
    usage_neg?: boolean;
    ecartd: number;
    pr_fin: string;
    f_long?: any;
    sens: string;
    proprietaire: string;
    id_perturbation_ligne?: number;
}

export class ReperageServerForSave {
    typeReperage: number;
    idDeviation: number;
    proprietaire: string;
    axe: string;
    sens: string;
    prDebut: string;
    prDebutDistance: number;
    prFin: string;
    prFinDistance: number;
    ecartd?: number;
    ecartf?: number;
    usageNeg: boolean;
    fSurf?: number;
    fLong?: number;

    constructor(reperageGridLine: ReperageGridLine) {
        this.typeReperage = 1;
        this.idDeviation = null;
        this.ecartd = 1;
        this.ecartf = 0;
        this.fSurf = null;
        this.fLong = null;
        this.proprietaire = reperageGridLine.axe.nom_complet.split(':')[0];
        this.axe = reperageGridLine.axe.nom_complet.split(':')[1];
        this.sens = reperageGridLine.axe.nom_complet.split(':')[2];
        this.prDebut = reperageGridLine.debutPr.secteur_nom;
        this.prDebutDistance = reperageGridLine.distanceDebut;
        this.prFin = reperageGridLine.finPr.secteur_nom;
        this.prFinDistance = reperageGridLine.distanceFin;
        this.usageNeg = false;
    }
}

export class ReperageGridLine implements IReperage {
    id?: number;
    fromDb?: boolean;
    drawn?: boolean;
    filteredAxeMaintenances?: IAxeMaintenance[];
    axe: IAxeMaintenance;
    debutPr: IPointRepere;
    distMaxDebut: number;
    distanceDebut: number;
    finPr: IPointRepere;
    distMaxFin: number;
    distanceFin: number;
    prDebuts?: IPointRepere[];
    prFins?: IPointRepere[];
    filteredPrDebuts?: any[];
    filteredPrFins?: any[];

    constructor(reperage: IReperage, axes: IAxeMaintenance[]) {
        this.id = reperage.id;
        if (axes) {
            this.filteredAxeMaintenances = axes;
        } else {
            this.filteredAxeMaintenances = [];
        }
        this.prDebuts = [];
        this.prFins = [];
        this.filteredPrDebuts = [];
        this.filteredPrFins = [];
    }

}


