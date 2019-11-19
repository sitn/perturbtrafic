export class Conflit {
    evenementId: number;
    evenementNumeroDossier: string;
    libelle: string;
    perturbationId: number;
    description: string;
    descriptionConflit: string;
    libelleConflit: string;
    evenementConflitId: number;
    evenementConflitNumeroDossier: string;
    perturbationConflitId: number;

    constructor(conflitServer: IConflitServer) {
        this.evenementId = conflitServer.id_evenement;
        this.evenementNumeroDossier = conflitServer.numero_dossier;
        this.evenementConflitId = conflitServer.id_evenement_conflit;
        this.evenementConflitNumeroDossier = conflitServer.numero_dossier_conflit;
        this.perturbationId = conflitServer.id_perturbation;
        this.perturbationConflitId = conflitServer.id_perturbation_conflit;
        this.descriptionConflit = conflitServer.description_conflit;
        this.libelleConflit = conflitServer.libelle_conflit;
        this.libelle = conflitServer.libelle;
        this.description = conflitServer.description;
    }
}

export interface IConflitServer {
    id_perturbation: number;
    description: string;
    id_evenement: number;
    numero_dossier: string;
    libelle: string;
    id_perturbation_conflit: number;
    description_conflit: string;
    id_evenement_conflit: number;
    numero_dossier_conflit: string;
    libelle_conflit: string;
}
