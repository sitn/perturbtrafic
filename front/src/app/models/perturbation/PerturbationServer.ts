import { DateUtils } from 'src/app/utils/date.utils';
import { PerturbationFormValues } from './IPerturbation';

export class PerturbationServer {
    id: number;
    id_evenement: number;
    // id_responsable_trafic: number;
    type: number;
    tranche_horaire: boolean;
    description: string;
    date_debut: Date;
    heure_debut: string;
    date_fin: Date;
    heure_fin: string;
    localisation: string;
    nom_responsable_trafic: string;
    prenom_responsable_trafic: string;
    mobile_responsable_trafic: string;
    telephone_responsable_trafic: string;
    fax_responsable_trafic: string;
    courriel_responsable_trafic: string;
    remarque: string;
    urgence: boolean;
    etat: number;
    date_validation: Date;
    utilisateur_validation: string;
    nom_utilisateur_validation: string;
    decision: string;
    date_decision: Date;
    id_utilisateur_ajout: number;
    nom_utilisateur_ajout: string;
    date_ajout: Date;
    id_utilisateur_modification: number;
    nom_utilisateur_modification: string;
    date_modification: Date;
    date_suppression: Date;

    constructor(perturbation: PerturbationFormValues) {
        // this.id = perturbation.id;
        this.id_evenement = perturbation.evenement.evenement;
        // this.id_responsable_trafic = perturbation.responsableTrafic.contact;
        this.type = perturbation.type;
        this.tranche_horaire = perturbation.trancheHoraire;
        this.description = perturbation.description;
        this.date_debut = perturbation.dates.dateDebut;
        this.heure_debut = perturbation.dates.heureDebut;
        this.date_fin = perturbation.dates.dateFin;
        this.heure_fin = perturbation.dates.heureFin;
        this.localisation = perturbation.localisation;
        this.nom_responsable_trafic = perturbation.responsableTrafic.contactInfos.nom;
        this.prenom_responsable_trafic = perturbation.responsableTrafic.contactInfos.prenom;
        this.mobile_responsable_trafic = perturbation.responsableTrafic.contactInfos.mobile;
        this.telephone_responsable_trafic = perturbation.responsableTrafic.contactInfos.telephone;
        this.fax_responsable_trafic = perturbation.responsableTrafic.contactInfos.fax;
        this.courriel_responsable_trafic = perturbation.responsableTrafic.contactInfos.courriel;
        this.remarque = perturbation.remarque;
        this.urgence = perturbation.urgence;
        this.etat = perturbation.etat;
        this.date_validation = perturbation.dateValidation;
        this.utilisateur_validation = perturbation.utilisateurValidation;
        this.decision = perturbation.decision;
        this.date_decision = perturbation.dateDecision;
        // this. id_utilisateur_ajout=perturbation.id;
        // this. date_ajout=perturbation.id;
        // this. id_utilisateur_modification=perturbation.id;
        // this. date_modification=perturbation.id;
        // this. date_suppression=perturbation.id;
    }
}

export abstract class PerturbationServerForSave {
    idPerturbation: number;
    idEvenement: number;
    idResponsableTrafic: number;
    type: number;
    trancheHoraire: string;
    description: string;
    dateDebut: string;
    heureDebut: string;
    dateFin: string;
    heureFin: string;
    localisation: string;
    nomResponsableTrafic: string;
    prenomResponsableTrafic: string;
    mobileResponsableTrafic: string;
    telephoneResponsableTrafic: string;
    faxResponsableTrafic: string;
    courrielResponsableTrafic: string;
    remarque: string;
    urgence: string;
    etat: number;
    dateValidation: string;
    utilisateurValidation: number;
    decision: string;
    dateDecision: string;
    ajoutePar: number;
    dateAjout: string;
    modifiePar: number;
    dateModification: string;
    dateSuppression: string;
    geometries_reperages: string;
    geometries_deviations: string;
    contacts_a_aviser: string;

    constructor(perturbation: PerturbationFormValues, geometries?: any[], deviations?: any[], contacts?: number[]) {
        this.idPerturbation = perturbation.id;
        this.idEvenement = perturbation.evenement.evenement;
        // this.idResponsableTrafic = perturbation.responsableTrafic.contact;
        this.type = perturbation.type;
        this.trancheHoraire = perturbation.trancheHoraire ? 'true' : 'false';
        this.description = perturbation.description;
        this.dateDebut = DateUtils.formatDate(perturbation.dates.dateDebut);
        this.heureDebut = DateUtils.formatTime(perturbation.dates.heureDebut);
        this.dateFin = DateUtils.formatDate(perturbation.dates.dateFin);
        this.heureFin = DateUtils.formatTime(perturbation.dates.heureFin);
        this.localisation = perturbation.localisation;
        this.nomResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.nom : null;
        this.prenomResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.prenom : null;
        this.mobileResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.mobile : null;
        this.telephoneResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.telephone : null;
        this.faxResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.fax : null;
        this.courrielResponsableTrafic = perturbation.responsableTrafic.contactInfos ? perturbation.responsableTrafic.contactInfos.courriel : null;
        this.remarque = perturbation.remarque;
        this.urgence = perturbation.urgence ? 'true' : 'false';
        this.etat = perturbation.etat;
        this.dateValidation = DateUtils.formatDate(perturbation.dateValidation);
        //this.  utilisateurValidation=perturbation.utilisateurValidation;
        this.decision = perturbation.decision;
        this.dateDecision = DateUtils.formatDate(perturbation.dateDecision);
        //this.  modifiePar=perturbation
        /* this.dateAjout = DateUtils.formatDate(new Date());
        this.dateModification = DateUtils.formatDate(new Date()); */
        this.geometries_reperages = JSON.stringify(geometries);
        this.geometries_deviations = JSON.stringify(deviations);
        if (contacts && contacts.length > 0) {
            this.contacts_a_aviser = JSON.stringify(contacts);
        }
    }
}
