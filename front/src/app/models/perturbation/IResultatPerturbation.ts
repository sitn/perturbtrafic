export interface IResultatPerturbationServer {
    id: number;
    axe: string;
    date_debut: string;
    heure_debut: string;
    date_fin: string;
    heure_fin: string;
    description: string;
    description_etat: string;
    description_evenement: string;
    description_type: string;
    description_type_evenement: string;
    deviation: string;
    tranche_horaire: boolean;
    etat: number;
    id_evenement: number;
    id_utilisateur_ajout: number;
    nom_utilisateur_ajout: string;
    numero_dossier_evenement: string;
    pr_debut: string;
    pr_fin: string;
    proprietaire_axe: string;
    sens: string;
    type: number;
    type_evenement: number;
    urgence: boolean;
    localisation_impression: string;
    suppression_autorise: boolean;
    modification_autorise: boolean;
    /* id: number;
    numero_dossier: string;
    localite: string;
    prevision: false;
    libelle: string;
    division: string;
    id_requerant: number;
    nom_requerant: string;
    id_responsable: number;
    nom_responsable: string;
    pr_touches: boolean; */
}

export class ResultatPerturbation {
    id?: number;
    numeroDossier: string;
    commune: string;
    typeEvenement: string;
    descriptionEvenement: string;
    deviation: string;
    trancheHoraire: boolean;
    urgence: boolean;
    description: string;
    etat: string;
    type: string;
    debut: Date;
    heureDebut: string;
    fin: Date;
    heureFin: string;
    localisationImpressionReperage: {
        id_evenement: string;
        axe: string;
        pr_debut: string;
        pr_debut_distance: string;
        pr_fin: string;
        pr_fin_distance: string;
    }[];
    localisationImpression: string;
    localisationImpressionExcel: string;
    modificationAutorisee: boolean;
    suppressionAutorisee: boolean;
    /* prevision: boolean;
    libelle: string;
    requerant: string;
    responsable: string;
    division: string; */

    constructor(resultatServer: IResultatPerturbationServer) {
        this.id = resultatServer.id;
        this.type = resultatServer.description_type;
        this.debut = new Date(resultatServer.date_debut);
        this.heureDebut = resultatServer.heure_debut;
        this.fin = new Date(resultatServer.date_fin);
        this.heureFin = resultatServer.heure_fin;
        this.typeEvenement = resultatServer.description_type_evenement;
        this.numeroDossier = resultatServer.numero_dossier_evenement;
        this.descriptionEvenement = resultatServer.description_evenement;
        this.description = resultatServer.description;
        this.etat = resultatServer.description_etat;
        this.urgence = resultatServer.urgence;
        this.trancheHoraire = resultatServer.tranche_horaire;
        this.deviation = resultatServer.deviation;
        this.modificationAutorisee = resultatServer.modification_autorise;
        this.suppressionAutorisee = resultatServer.suppression_autorise;
        if (resultatServer.localisation_impression) {
            try {
                this.localisationImpressionReperage = JSON.parse(resultatServer.localisation_impression);
                this.localisationImpressionReperage.forEach((rep, index) => {
                    if (index === 0) {
                        this.localisationImpressionExcel = rep.axe +
                            rep.pr_debut + rep.pr_debut_distance + rep.pr_fin + rep.pr_fin_distance;
                    } else {
                        this.localisationImpressionExcel = this.localisationImpressionExcel + '\r\n' + rep.axe +
                            rep.pr_debut + rep.pr_debut_distance + rep.pr_fin + rep.pr_fin_distance;
                    }
                });
            } catch (e) {
                this.localisationImpression = resultatServer.localisation_impression;
                this.localisationImpressionExcel = resultatServer.localisation_impression;
            }
        }
        // this.commune = resultatServer.localite;
        // this = resultatServer.description_type;
        // this.prevision = resultatServer.prevision;
        // this.libelle = resultatServer.libelle;
        /* this.requerant = resultatServer.nom_requerant;
        this.responsable = resultatServer.nom_responsable;
        this.division = resultatServer.division; */
    }
}
