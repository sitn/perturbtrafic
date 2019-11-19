export class EvenementEcheance {
    id: number;
    numeroDossier: string;
    libelle: string;
    dateDebut: Date;

    constructor(evenementEcheanceServer: IEvenementEcheanceServer) {
        this.id = evenementEcheanceServer.id;
        this.numeroDossier = evenementEcheanceServer.numero_dossier;
        this.libelle = evenementEcheanceServer.libelle;
        if (evenementEcheanceServer.date_debut) {
            this.dateDebut = new Date(evenementEcheanceServer.date_debut);
        }
    }
}

export interface IEvenementEcheanceServer {
    id: number;
    numero_dossier: string;
    libelle: string;
    date_debut: string;
}
