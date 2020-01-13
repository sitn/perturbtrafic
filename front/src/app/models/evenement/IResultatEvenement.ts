export interface IResultatEvenementServer {
    id: number;
    numero_dossier: string;
    localisation: string;
    type: number;
    description_type: string;
    description: string;
    prevision: false;
    libelle: string;
    date_debut: Date;
    date_fin: Date;
    division: string;
    id_requerant: number;
    nom_requerant: string;
    id_responsable: number;
    nom_responsable: string;
    proprietaire: string;
    axe: string;
    sens: string;
    pr_debut: string;
    pr_fin: string;
    id_utilisateur_ajout: number;
    nom_utilisateur_ajout: string;
    pr_touches: boolean;
    localisation_impression: string;
    suppression_autorise: boolean;
    modification_autorise: boolean;
}

export interface IResultatEvenement {
    id?: number;
    numeroDossier: string;
    localisation: string;
    typeEvenement: string;
    description: string;
    prevision: boolean;
    libelle: string;
    requerant: string;
    responsable: string;
    division: string;
    debut: Date;
    fin: Date;
    localisationImpression: any;
}

export class ResultatEvenement implements IResultatEvenement {
    id?: number;
    numeroDossier: string;
    localisation: string;
    description: string;
    typeEvenement: string;
    prevision: boolean;
    libelle: string;
    requerant: string;
    responsable: string;
    division: string;
    debut: Date;
    fin: Date;
    localisationImpressionReperage: {
        id_evenement: string;
        axe: string;
        pr_debut: string;
        pr_debut_distance: string;
        pr_fin: string;
        pr_fin_distance: string;
    }[];
    localisationImpressionExcel: string;
    localisationImpression: string;
    modificationAutorisee: boolean;
    suppressionAutorisee: boolean;

    constructor(resultatServer: IResultatEvenementServer) {
        this.id = resultatServer.id;
        this.numeroDossier = resultatServer.numero_dossier;
        this.description = resultatServer.description;
        this.localisation = resultatServer.localisation;
        this.typeEvenement = resultatServer.description_type;
        this.prevision = resultatServer.prevision;
        this.libelle = resultatServer.libelle;
        this.requerant = resultatServer.nom_requerant;
        this.responsable = resultatServer.nom_responsable;
        this.division = resultatServer.division;
        this.debut = new Date(resultatServer.date_debut);
        this.fin = new Date(resultatServer.date_fin);
        this.modificationAutorisee = resultatServer.modification_autorise;
        this.suppressionAutorisee = resultatServer.suppression_autorise;
        if (resultatServer.localisation_impression) {
            try {
                this.localisationImpressionExcel = '';
                this.localisationImpressionReperage = JSON.parse(resultatServer.localisation_impression);
                this.localisationImpressionReperage.forEach((rep, index) => {
                    if (index === 0) {
                        this.localisationImpressionExcel = rep.axe + ' de ' +
                            rep.pr_debut + rep.pr_debut_distance + ' à ' + rep.pr_fin + rep.pr_fin_distance;
                    } else {
                        this.localisationImpressionExcel = this.localisationImpressionExcel + '\r\n' + rep.axe + ' de ' +
                            rep.pr_debut + rep.pr_debut_distance + ' à ' + rep.pr_fin + rep.pr_fin_distance;
                    }
                });
            } catch (e) {
                this.localisationImpression = resultatServer.localisation_impression;
                this.localisationImpressionExcel = resultatServer.localisation_impression;
            }
            // this.localisationImpressionReperage = 'bonjour \r\n c est nico';
        }
    }
}
