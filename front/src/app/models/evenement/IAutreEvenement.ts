import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { DateUtils } from 'src/app/utils/date.utils';

import { ContactFormGroup, ContactFormValues, IContact } from '../IContact';
import { IOrganisme, OrganismeFormGroup, OrganismeFormValues } from '../IOrganisme';
import { EvenementServerForSave } from './EvenementServer';
import { EvenementFormValues } from './IEvenementForm';
import { IUser } from '../IUser';

export interface IAutreEvenement {
    maitreOuvrage: IOrganisme;
    directionLocale: IContact;
    entrepreneur: IOrganisme;
    responsableTravaux: IContact;
    cause: string;
    facturation: string;
    dateDebutValide: Date;
    dateFinValide: Date;
    dateMajValide: Date;
    numeroFacture: string;
    dateFacture: Date;
    reserveEventuelle: string;
}

export class AutreEvenementFormGroup {
    maitreOuvrage = new FormBuilder().group(
        new OrganismeFormGroup()
    );
    directionLocale = new FormBuilder().group(
        new ContactFormGroup()
    );
    entrepreneur = new FormBuilder().group(
        new OrganismeFormGroup()
    );
    responsableTravaux = new FormBuilder().group(
        new ContactFormGroup()
    );
    cause = new FormControl(null, Validators.maxLength(50));
    facturation = new FormControl();
    dateDebutValide = new FormControl();
    dateFinValide = new FormControl();
    dateMajValide = new FormControl();
    numeroFacture = new FormControl(null, Validators.maxLength(50));
    dateFacture = new FormControl();
    reserveEventuelle = new FormControl(null, Validators.maxLength(500));
}


export class AutreEvenementFormValues {
    maitreOuvrage: OrganismeFormValues;
    directionLocale: ContactFormValues;
    entrepreneur: OrganismeFormValues;
    responsableTravaux: ContactFormValues;
    cause: string;
    facturation: number;
    dateDebutValide: Date;
    dateFinValide: Date;
    dateMajValide: Date;
    numeroFacture: string;
    dateFacture: Date;
    reserveEventuelle: string;

    constructor(autreEvenementInfos: AutreEvenementServerEdition) {
        this.maitreOuvrage = new OrganismeFormValues(
            autreEvenementInfos.id_maitre_ouvrage,
            autreEvenementInfos.nom_maitre_ouvrage,
            autreEvenementInfos.rue_maitre_ouvrage,
            autreEvenementInfos.localite_maitre_ouvrage,
            autreEvenementInfos.telephone_maitre_ouvrage,
            autreEvenementInfos.fax_maitre_ouvrage,
            autreEvenementInfos.courriel_maitre_ouvrage
        );
        this.directionLocale = new ContactFormValues(
            autreEvenementInfos.id_direction_locale,
            autreEvenementInfos.nom_direction_locale,
            autreEvenementInfos.prenom_direction_locale,
            autreEvenementInfos.mobile_direction_locale,
            autreEvenementInfos.telephone_direction_locale,
            autreEvenementInfos.fax_direction_locale,
            autreEvenementInfos.courriel_direction_locale
        );
        this.entrepreneur = new OrganismeFormValues(
            autreEvenementInfos.id_entrepreneur,
            autreEvenementInfos.nom_entrepreneur,
            autreEvenementInfos.rue_entrepreneur,
            autreEvenementInfos.localite_entrepreneur,
            autreEvenementInfos.telephone_entrepreneur,
            autreEvenementInfos.fax_entrepreneur,
            autreEvenementInfos.courriel_entrepreneur
        );
        this.responsableTravaux = new ContactFormValues(
            autreEvenementInfos.id_responsable_travaux,
            autreEvenementInfos.nom_responsable_travaux,
            autreEvenementInfos.prenom_responsable_travaux,
            autreEvenementInfos.mobile_responsable_travaux,
            autreEvenementInfos.telephone_responsable_travaux,
            autreEvenementInfos.fax_responsable_travaux,
            autreEvenementInfos.courriel_responsable_travaux
        );
        this.cause = autreEvenementInfos.cause;
        this.facturation = autreEvenementInfos.facturation;
        this.dateDebutValide = autreEvenementInfos.date_debut_valide ? new Date(autreEvenementInfos.date_debut_valide) : null;
        this.dateFinValide = autreEvenementInfos.date_fin_valide ? new Date(autreEvenementInfos.date_fin_valide) : null;
        this.dateMajValide = autreEvenementInfos.date_maj_valide ? new Date(autreEvenementInfos.date_maj_valide) : null;
        this.numeroFacture = autreEvenementInfos.numero_facture;
        this.dateFacture = autreEvenementInfos.date_facture ? new Date(autreEvenementInfos.date_facture) : null;
        this.reserveEventuelle = autreEvenementInfos.reserve_eventuelle;
    }
}

export class AutreEvenementServerEdition {
    cause: string;
    coordonnes_x: number;
    coordonnes_y: number;
    courriel_direction_locale: string;
    courriel_entrepreneur: string;
    courriel_maitre_ouvrage: string;
    courriel_responsable_travaux: string;
    date_debut_valide: Date;
    date_facture: Date;
    date_fin_valide: Date;
    date_maj_valide: Date;
    facturation: number;
    fax_direction_locale: string;
    fax_entrepreneur: string;
    fax_maitre_ouvrage: string;
    fax_responsable_travaux: string;
    id?: number;
    id_direction_locale: number;
    id_entrepreneur: number;
    id_evenement?: number;
    id_maitre_ouvrage: number;
    id_responsable_travaux: number;
    localite_entrepreneur: string;
    localite_maitre_ouvrage: string;
    mobile_direction_locale: string;
    mobile_responsable_travaux: string;
    nom_direction_locale: string;
    nom_entrepreneur: string;
    nom_maitre_ouvrage: string;
    nom_responsable_travaux: string;
    numero_facture: string;
    prenom_direction_locale: string;
    prenom_responsable_travaux: string;
    reserve_eventuelle: string;
    rue_entrepreneur: string;
    rue_maitre_ouvrage: string;
    telephone_direction_locale: string;
    telephone_entrepreneur: string;
    telephone_maitre_ouvrage: string;
    telephone_responsable_travaux: string;
}

export class AutreEvenementServerSave extends EvenementServerForSave {
    _idMaitreOuvrage: number;
    _idDirectionLocale: number;
    _idEntrepreneur: number;
    _idResponsableTravaux: number;
    _cause: string;
    _nomMaitreOuvrage: string;
    _rueMaitreOuvrage: string;
    _localiteMaitreOuvrage: string;
    _telephoneMaitreOuvrage: string;
    _faxMaitreOuvrage: string;
    _courrielMaitreOuvrage: string;
    _nomDirectionLocale: string;
    _prenomDirectionLocale: string;
    _mobileDirectionLocale: string;
    _telephoneDirectionLocale: string;
    _faxDirectionLocale: string;
    _courrielDirectionLocale: string;
    _nomEntrepreneur: string;
    _rueEntrepreneur: string;
    _localiteEntrepreneur: string;
    _telephoneEntrepreneur: string;
    _faxEntrepreneur: string;
    _courrielEntrepreneur: string;
    _nomResponsableTravaux: string;
    _prenomResponsableTravaux: string;
    _mobileResponsableTravaux: string;
    _telephoneResponsableTravaux: string;
    _faxResponsableTravaux: string;
    _courrielResponsableTravaux: string;
    _facturation: number;
    _coordonnesX: number;
    _coordonnesY: number;
    _dateDebutValide: string;
    _dateFinValide: string;
    _dateMajValide: string;
    _numeroFacture: string;
    _dateFacture: string;
    _reserveEventuelle: string;

    constructor(evenementValue: EvenementFormValues, user: IUser, geometries?: any[]) {
        super(evenementValue, user, geometries);
        const autreEvenementValue = evenementValue.autre;
        // this._idMaitreOuvrage = autreEvenementValue.maitreOuvrage.organisme;
        // this._idDirectionLocale = autreEvenementValue.directionLocale.contact;
        // this._idEntrepreneur = autreEvenementValue.entrepreneur.organisme;
        // this._idResponsableTravaux = autreEvenementValue.responsableTravaux.contact;
        this._cause = autreEvenementValue.cause;
        this._nomMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.nom;
        this._rueMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.adresse;
        this._localiteMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.localite;
        this._telephoneMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.telephone;
        this._faxMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.fax;
        this._courrielMaitreOuvrage = autreEvenementValue.maitreOuvrage.contactInfos.courriel;
        this._nomDirectionLocale = autreEvenementValue.directionLocale.contactInfos.nom;
        this._prenomDirectionLocale = autreEvenementValue.directionLocale.contactInfos.prenom;
        this._mobileDirectionLocale = autreEvenementValue.directionLocale.contactInfos.mobile;
        this._telephoneDirectionLocale = autreEvenementValue.directionLocale.contactInfos.telephone;
        this._faxDirectionLocale = autreEvenementValue.directionLocale.contactInfos.fax;
        this._courrielDirectionLocale = autreEvenementValue.directionLocale.contactInfos.courriel;
        this._nomEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.nom;
        this._rueEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.adresse;
        this._localiteEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.localite;
        this._telephoneEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.telephone;
        this._faxEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.fax;
        this._courrielEntrepreneur = autreEvenementValue.entrepreneur.contactInfos.courriel;
        this._nomResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.nom;
        this._prenomResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.prenom;
        this._mobileResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.mobile;
        this._telephoneResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.telephone;
        this._faxResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.fax;
        this._courrielResponsableTravaux = autreEvenementValue.responsableTravaux.contactInfos.courriel;
        this._facturation = autreEvenementValue.facturation;
        this._dateDebutValide = DateUtils.formatDate(autreEvenementValue.dateDebutValide);
        this._dateFinValide = DateUtils.formatDate(autreEvenementValue.dateFinValide);
        this._dateMajValide = DateUtils.formatDate(autreEvenementValue.dateMajValide);
        this._numeroFacture = autreEvenementValue.numeroFacture;
        this._dateFacture = DateUtils.formatDate(autreEvenementValue.dateFacture);
        this._reserveEventuelle = autreEvenementValue.reserveEventuelle;
    }
}
