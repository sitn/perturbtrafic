import { DateUtils } from 'src/app/utils/date.utils';
import { EvenementFormValues } from './IEvenementForm';
import { IUser } from '../IUser';

export class EvenementServer {
    id: number;
    id_entite: number;
    id_responsable: number;
    id_requerant: number;
    type: number;
    numero_dossier: string;
    division: string;
    libelle: string;
    description: string;
    prevision: boolean;
    date_debut: Date;
    heure_debut: string;
    date_fin: Date;
    heure_fin: string;
    localisation: string;
    reperage_effectif: boolean;
    nom_requerant: string;
    rue_requerant: string;
    localite_requerant: string;
    telephone_requerant: string;
    fax_requerant: string;
    courriel_requerant: string;
    nom_contact: string;
    prenom_contact: string;
    mobile_contact: string;
    telephone_contact: string;
    fax_contact: string;
    courriel_contact: string;
    remarque: string;
    date_demande: string;
    date_octroi: string;
    id_utilisateur_ajout: number;
    nom_utilisateur_ajout: string;
    date_ajout: Date;
    id_utilisateur_modification: number;
    nom_utilisateur_modification: string;
    date_modification: Date;
    date_suppression: Date;

    constructor(evenement: EvenementFormValues) {
        this.id = evenement.id;
        this.id_entite = evenement.id;
        this.id_responsable = evenement.id;
        this.id_requerant = evenement.id;
        this.type = evenement.id;
        this.numero_dossier = evenement.numeroDossier;
        this.division = evenement.division;
        this.libelle = evenement.libelle;
        this.description = evenement.description;
        this.prevision = evenement.prevision;
        this.date_debut = evenement.dates.dateDebut;
        this.heure_debut = evenement.dates.heureDebut;
        this.date_fin = evenement.dates.dateFin;
        this.heure_fin = evenement.dates.heureFin;
        this.localisation = evenement.localisation;
        this.type = evenement.type.type;
        /* this.nom_requerant = evenement.requerant;
        this.rue_requerant = evenement.id;
        this.localite_requerant = evenement.id;
        this.telephone_requerant = evenement.id;
        this.fax_requerant = evenement.id;
        this.courriel_requerant = evenement.id; */
        /* this.nom_contact = evenement.id;
        this.prenom_contact = evenement.id;
        this.mobile_contact = evenement.id;
        this.telephone_contact = evenement.id;
        this.fax_contact = evenement.id;
        this.courriel_contact = evenement.id; */
        this.remarque = evenement.remarque;
        this.date_demande = DateUtils.formatDate(evenement.dateDemande);
        this.date_octroi = DateUtils.formatDate(evenement.dateOctroi);
        // this.id_utilisateur_ajout = evenement.utilisateurAjout;
        // this.date_ajout = formatDate(evenement.dateAjout);
        this.id_utilisateur_modification = evenement.id;
        // this.date_modification = DateUtils.formatDate(new Date());
        // this.date_suppression = formatDate(evenement.dateAjout);
    }
}


export abstract class EvenementServerForSave {
    idEvenement?: number;
    idEntite: number;
    idResponsable: number;
    idRequerant: number;
    type: number;
    numeroDossier: string;
    division: string;
    libelle: string;
    description: string;
    prevision: string;
    dateDebut: string;
    heureDebut: string;
    dateFin: string;
    heureFin: string;
    localisation: string;
    nomRequerant: string;
    rueRequerant: string;
    localiteRequerant: string;
    telephoneRequerant: string;
    faxRequerant: string;
    courrielRequerant: string;
    nomContact: string;
    prenomContact: string;
    mobileContact: string;
    telephoneContact: string;
    faxContact: string;
    courrielContact: string;
    remarque: string;
    dateDemande: string;
    dateOctroi: string;
    ajoutePar: number;
    dateAjout: string;
    modifiePar: number;
    dateModification: string;
    dateSuppression: string;
    geometries_reperages: string;
    // Autre
    // Manifestation
    _parcours?: string;


    constructor(evenement: EvenementFormValues, user: IUser, geometries?: any[]) {
        this.idEvenement = evenement.id;
        if (user && user.currentEntity) {
            this.idEntite = user.currentEntity.id;
        }
        this.idResponsable = evenement.responsable;
        this.type = evenement.type.type;
        this.numeroDossier = evenement.numeroDossier;
        this.division = evenement.division;
        this.libelle = evenement.libelle;
        this.description = evenement.description;
        this.prevision = evenement.prevision ? 'true' : 'false';
        this.dateDebut = DateUtils.formatDate(evenement.dates.dateDebut);
        this.heureDebut = DateUtils.formatTime(evenement.dates.heureDebut);
        // this.heureDebut = '08:00:00';
        this.dateFin = DateUtils.formatDate(evenement.dates.dateFin);
        this.heureFin = DateUtils.formatTime(evenement.dates.heureFin);
        // this.heureFin = '08:00:00';
        this.localisation = evenement.localisation;
        this.nomRequerant = evenement.requerant.contactInfos.nom;
        this.rueRequerant = evenement.requerant.contactInfos.adresse;
        this.localiteRequerant = evenement.requerant.contactInfos.localite;
        this.telephoneRequerant = evenement.requerant.contactInfos.telephone;
        this.faxRequerant = evenement.requerant.contactInfos.fax;
        this.courrielRequerant = evenement.requerant.contactInfos.courriel;
        this.nomContact = evenement.contact.contactInfos.nom;
        this.prenomContact = evenement.contact.contactInfos.prenom;
        this.mobileContact = evenement.contact.contactInfos.mobile;
        this.telephoneContact = evenement.contact.contactInfos.telephone;
        this.faxContact = evenement.contact.contactInfos.fax;
        this.courrielContact = evenement.contact.contactInfos.courriel;
        this.remarque = evenement.remarque;
        this.dateDemande = DateUtils.formatDate(evenement.dateDemande);
        this.dateOctroi = DateUtils.formatDate(evenement.dateOctroi);
        this.dateAjout = DateUtils.formatDate(new Date());
        this.dateModification = DateUtils.formatDate(new Date());
        this.geometries_reperages = JSON.stringify(geometries); // this.dateSuppression = evenement.d;
        // this._parcours = evenement.p;

        // Autre
        /* if (evenement.type.type === 1) {
            this._parcours = evenement.manifestation.parcours;
        } else
            // Manifestation
            if (evenement.type.type === 4) {
                this._parcours = evenement.manifestation.parcours;
            } */
    }
}
