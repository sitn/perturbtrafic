import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { DateUtils } from 'src/app/utils/date.utils';

import { ContactFormGroup, ContactFormValues, IContact } from '../IContact';
import { IOrganisme, OrganismeFormGroup, OrganismeFormValues } from '../IOrganisme';
import { EvenementFormValues } from './IEvenementForm';
import { EvenementServerForSave } from './EvenementServer';
import { IUser } from '../IUser';

export class FouilleFormGroup {

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
    facturation = new FormControl();
    prTouches = new FormControl(false, Validators.required);
    longueurEtape = new FormControl();
    epaisseurCaisson = new FormControl();
    qualiteCaisson = new FormControl(null, Validators.maxLength(50));
    epaisseurSupport = new FormControl();
    qualiteSupport = new FormControl(null, Validators.maxLength(50));
    epaisseurRevetement = new FormControl();
    qualiteRevetement = new FormControl(null, Validators.maxLength(50));
    qualiteEncollage = new FormControl(null, Validators.maxLength(100));
    planType = new FormControl(null, Validators.maxLength(200));
    dateDebutValide = new FormControl();
    dateFinValide = new FormControl();
    dateMajValide = new FormControl();
    numeroFacture = new FormControl(null, Validators.maxLength(50));
    dateFacture = new FormControl();
    reserveEventuelle = new FormControl(null, Validators.maxLength(500));
    reperageEffectif = new FormControl(false, Validators.required);

    /* constructor() { } */

}

export class FouilleFormValues {
    maitreOuvrage: OrganismeFormValues;
    directionLocale: ContactFormValues;
    entrepreneur: OrganismeFormValues;
    responsableTravaux: ContactFormValues;
    facturation: string;
    prTouches: boolean;
    longueurEtape: number;
    epaisseurCaisson: number;
    qualiteCaisson: string;
    epaisseurSupport: number;
    qualiteSupport: string;
    epaisseurRevetement: number;
    qualiteRevetement: string;
    qualiteEncollage: string;
    planType: number[];
    dateDebutValide: Date;
    dateFinValide: Date;
    dateMajValide: Date;
    numeroFacture: string;
    dateFacture: Date;
    reserveEventuelle: string;
    reperageEffectif: boolean;

    constructor(fouille: FouilleServerEdition, plansType: any[]) {
        this.maitreOuvrage = new OrganismeFormValues(
            fouille.id_maitre_ouvrage,
            fouille.nom_maitre_ouvrage,
            fouille.rue_maitre_ouvrage,
            fouille.localite_maitre_ouvrage,
            fouille.telephone_maitre_ouvrage,
            fouille.fax_maitre_ouvrage,
            fouille.courriel_maitre_ouvrage
        );
        this.directionLocale = new ContactFormValues(
            fouille.id_direction_locale,
            fouille.nom_direction_locale,
            fouille.prenom_direction_locale,
            fouille.mobile_direction_locale,
            fouille.telephone_direction_locale,
            fouille.fax_direction_locale,
            fouille.courriel_direction_locale
        );
        this.entrepreneur = new OrganismeFormValues(
            fouille.id_entrepreneur,
            fouille.nom_entrepreneur,
            fouille.rue_entrepreneur,
            fouille.localite_entrepreneur,
            fouille.telephone_entrepreneur,
            fouille.fax_entrepreneur,
            fouille.courriel_entrepreneur
        );
        this.responsableTravaux = new ContactFormValues(
            fouille.id_responsable_travaux,
            fouille.nom_responsable_travaux,
            fouille.prenom_responsable_travaux,
            fouille.mobile_responsable_travaux,
            fouille.telephone_responsable_travaux,
            fouille.fax_responsable_travaux,
            fouille.courriel_responsable_travaux
        );
        this.facturation = fouille.facturation;
        this.prTouches = fouille.pr_touches;
        this.longueurEtape = fouille.longueur_etape;
        this.epaisseurCaisson = fouille.epaisseur_caisson;
        this.qualiteCaisson = fouille.qualite_caisson;
        this.epaisseurSupport = fouille.epaisseur_caisson;
        this.qualiteSupport = fouille.qualite_support;
        this.epaisseurRevetement = fouille.epaisseur_revetement;
        this.qualiteRevetement = fouille.qualite_revetement;
        this.qualiteEncollage = fouille.qualite_encollage;
        this.dateDebutValide = fouille.date_debut_valide ? new Date(fouille.date_debut_valide) : null;
        this.dateFinValide = fouille.date_fin_valide ? new Date(fouille.date_fin_valide) : null;
        this.dateMajValide = fouille.date_maj_valide ? new Date(fouille.date_maj_valide) : null;
        this.numeroFacture = fouille.numero_facture;
        this.dateFacture = fouille.date_facture ? new Date(fouille.date_facture) : null;
        this.reserveEventuelle = fouille.facturation;
        this.reperageEffectif = fouille.reperage_effectif;
        this.planType = [];
        if (plansType && plansType.length > 0) {
            plansType.forEach(plan => {
                this.planType.push(plan.id);
            });
        }

    }


}

export class FouilleServerEdition {
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
    epaisseur_caisson: number;
    epaisseur_revetement: number;
    epaisseur_support: number;
    facturation: string;
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
    longueur_etape: number;
    mobile_direction_locale: string;
    mobile_responsable_travaux: string;
    nom_direction_locale: string;
    nom_entrepreneur: string;
    nom_maitre_ouvrage: string;
    nom_responsable_travaux: string;
    numero_facture: string;
    plan_type: string;
    pr_touches: boolean;
    prenom_direction_locale: string;
    prenom_responsable_travaux: string;
    qualite_caisson: string;
    qualite_encollage: string;
    qualite_revetement: string;
    qualite_support: string;
    reperage_effectif: boolean;
    reserve_eventuelle: string;
    rue_entrepreneur: string;
    rue_maitre_ouvrage: string;
    telephone_direction_locale: string;
    telephone_entrepreneur: string;
    telephone_maitre_ouvrage: string;
    telephone_responsable_travaux: string;
}

export class FouilleServerSave extends EvenementServerForSave {
    _idMaitreOuvrage: number;
    _idDirectionLocale: number;
    _idEntrepreneur: number;
    _idResponsableTravaux: number;
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
    _facturation: string;
    _coordonnesX: number;
    _coordonnesY: number;
    _prTouches: string;
    _longueurEtape: number;
    _epaisseurCaisson: number;
    _qualiteCaisson: string;
    _epaisseurSupport: number;
    _qualiteSupport: string;
    _epaisseurRevetement: number;
    _qualiteRevetement: string;
    _qualiteEncollage: string;
    _planTypes: string;
    _dateDebutValide: string;
    _dateFinValide: string;
    _dateMajValide: string;
    _numeroFacture: string;
    _dateFacture: string;
    _reserveEventuelle: string;
    _reperageEffectif: string;

    constructor(evenement: EvenementFormValues, user: IUser, geometries?: any[]) {
        super(evenement, user, geometries);
        const fouille = evenement.fouille;
        // this._idMaitreOuvrage = fouille.maitreOuvrage.organisme;
        // this._idDirectionLocale = fouille.directionLocale.contact;
        // this._idEntrepreneur = fouille.entrepreneur.organisme;
        // this._idResponsableTravaux = fouille.responsableTravaux.contact;
        this._nomMaitreOuvrage = fouille.maitreOuvrage.contactInfos.nom;
        this._rueMaitreOuvrage = fouille.maitreOuvrage.contactInfos.adresse;
        this._localiteMaitreOuvrage = fouille.maitreOuvrage.contactInfos.localite;
        this._telephoneMaitreOuvrage = fouille.maitreOuvrage.contactInfos.telephone;
        this._faxMaitreOuvrage = fouille.maitreOuvrage.contactInfos.fax;
        this._courrielMaitreOuvrage = fouille.maitreOuvrage.contactInfos.courriel;
        this._nomDirectionLocale = fouille.directionLocale.contactInfos.nom;
        this._prenomDirectionLocale = fouille.directionLocale.contactInfos.prenom;
        this._mobileDirectionLocale = fouille.directionLocale.contactInfos.mobile;
        this._telephoneDirectionLocale = fouille.directionLocale.contactInfos.telephone;
        this._faxDirectionLocale = fouille.directionLocale.contactInfos.fax;
        this._courrielDirectionLocale = fouille.directionLocale.contactInfos.courriel;
        this._nomEntrepreneur = fouille.entrepreneur.contactInfos.nom;
        this._rueEntrepreneur = fouille.entrepreneur.contactInfos.adresse;
        this._localiteEntrepreneur = fouille.entrepreneur.contactInfos.localite;
        this._telephoneEntrepreneur = fouille.entrepreneur.contactInfos.telephone;
        this._faxEntrepreneur = fouille.entrepreneur.contactInfos.fax;
        this._courrielEntrepreneur = fouille.entrepreneur.contactInfos.courriel;
        this._nomResponsableTravaux = fouille.responsableTravaux.contactInfos.nom;
        this._prenomResponsableTravaux = fouille.responsableTravaux.contactInfos.prenom;
        this._mobileResponsableTravaux = fouille.responsableTravaux.contactInfos.mobile;
        this._telephoneResponsableTravaux = fouille.responsableTravaux.contactInfos.telephone;
        this._faxResponsableTravaux = fouille.responsableTravaux.contactInfos.fax;
        this._courrielResponsableTravaux = fouille.responsableTravaux.contactInfos.courriel;
        this._facturation = fouille.facturation;
        this._prTouches = fouille.prTouches ? 'true' : 'false';
        this._reperageEffectif = fouille.reperageEffectif ? 'true' : 'false';
        this._longueurEtape = fouille.longueurEtape;
        this._epaisseurCaisson = fouille.epaisseurCaisson;
        this._qualiteCaisson = fouille.qualiteCaisson;
        this._epaisseurSupport = fouille.epaisseurSupport;
        this._qualiteSupport = fouille.qualiteSupport;
        this._epaisseurRevetement = fouille.epaisseurRevetement;
        this._qualiteRevetement = fouille.qualiteRevetement;
        this._qualiteEncollage = fouille.qualiteEncollage;
        if (fouille.planType && fouille.planType.length > 0) {
            this._planTypes = JSON.stringify(fouille.planType);
        }
        this._dateDebutValide = DateUtils.formatDate(fouille.dateDebutValide);
        this._dateFinValide = DateUtils.formatDate(fouille.dateFinValide);
        this._dateMajValide = DateUtils.formatDate(fouille.dateMajValide);
        this._numeroFacture = fouille.numeroFacture;
        this._dateFacture = DateUtils.formatDate(fouille.dateFacture);
        this._reserveEventuelle = fouille.reserveEventuelle;
    }
}

export interface IFouille {
    maitreOuvrage: IOrganisme;
    directionLocale: IContact;
    entrepreneur: IOrganisme;
    responsableTravaux: IContact;
    facturation: string;
    prTouches: boolean;
    longueurEtape: string;
    epaisseurCaisson: string;
    qualiteCaisson: string;
    epaisseurSupport: string;
    qualiteSupport: string;
    epaisseurRevetement: number;
    qualiteRevetement: string;
    qualiteEncollage: string;
    planType: string;
    dateDebutValide: Date;
    dateFinValide: Date;
    dateMajValide: Date;
    numeroFacture: string;
    dateFacture: Date;
    reserveEventuelle: string;
    reperageEffectif: boolean;
}

export interface IPlanTypeFouille {
    id: number;
    description: string;
}


