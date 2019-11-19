import { FormControl, Validators } from '@angular/forms';

import { IContact } from '../IContact';
import { IOrganisme } from '../IOrganisme';
import { EvenementServerForSave } from './EvenementServer';
import { EvenementFormValues } from './IEvenementForm';
import { DateUtils } from 'src/app/utils/date.utils';

export class ChantierFormGroup {
    maitreOuvrage = new FormControl();
    directionLocale = new FormControl();
    entrepreneur = new FormControl();
    responsableTravaux = new FormControl();
    projet = new FormControl(null, Validators.maxLength(100));
    longueurEtape = new FormControl(null, Validators.maxLength(50));
    surface = new FormControl(null, Validators.maxLength(50));
    centraleEnrobage = new FormControl();
    epaisseurCaisson = new FormControl(null, Validators.maxLength(50));
    qualiteCaisson = new FormControl(null, Validators.maxLength(50));
    epaisseurSupport = new FormControl(null, Validators.maxLength(50));
    qualiteSupport = new FormControl(null, Validators.maxLength(50));
    epaisseurRevetement = new FormControl(null, Validators.maxLength(50));
    qualiteRevetement = new FormControl(null, Validators.maxLength(50));
    qualiteEncollage = new FormControl(null, Validators.maxLength(100));
    boucleInduction = new FormControl(false, Validators.required);
    faucherAccotement = new FormControl(false, Validators.required);
    curerDepotoirs = new FormControl(false, Validators.required);
    nettoyerBords = new FormControl(false, Validators.required);
    colmaterFissure = new FormControl(false, Validators.required);
    prTouches = new FormControl(false, Validators.required);
    autre = new FormControl(null, Validators.maxLength(500));
    lieuSeance = new FormControl(null, Validators.maxLength(100));
    jourSeance = new FormControl();
    heureSeance = new FormControl(null, Validators.maxLength(50));
    categorie = new FormControl();
    reperageEffectif = new FormControl(false, Validators.required);
}

export class ChantierFormValues {
    maitreOuvrage: number;
    directionLocale: number;
    entrepreneur: number;
    responsableTravaux: number;
    projet: string;
    longueurEtape: number;
    surface: number;
    centraleEnrobage: number;
    epaisseurCaisson: string;
    qualiteCaisson: string;
    epaisseurSupport: string;
    qualiteSupport: string;
    epaisseurRevetement: string;
    qualiteRevetement: string;
    qualiteEncollage: string;
    boucleInduction: boolean;
    faucherAccotement: boolean;
    curerDepotoirs: boolean;
    nettoyerBords: boolean;
    colmaterFissure: boolean;
    prTouches: boolean;
    autre: string;
    lieuSeance: string;
    jourSeance: string;
    heureSeance: string;
    categorie: number[];
    reperageEffectif: boolean;

    constructor(chantierServer: IChantierServerEdition, categoriesChantier: any[]) {
        this.maitreOuvrage = chantierServer.id_maitre_ouvrage;
        this.directionLocale = chantierServer.id_direction_locale;
        this.entrepreneur = chantierServer.id_entrepreneur;
        this.responsableTravaux = chantierServer.id_responsable_travaux;
        this.projet = chantierServer.projet;
        this.longueurEtape = chantierServer.longueur_etape;
        this.surface = chantierServer.surface;
        this.centraleEnrobage = chantierServer.id_centrale_enrobage;
        this.epaisseurCaisson = chantierServer.epaisseur_caisson;
        this.qualiteCaisson = chantierServer.qualite_caisson;
        this.epaisseurSupport = chantierServer.epaisseur_caisson;
        this.qualiteSupport = chantierServer.qualite_support;
        this.epaisseurRevetement = chantierServer.epaisseur_revetement;
        this.qualiteRevetement = chantierServer.qualite_revetement;
        this.qualiteEncollage = chantierServer.qualite_encollage;
        this.boucleInduction = chantierServer.boucle_induction;
        this.faucherAccotement = chantierServer.faucher_accotement;
        this.curerDepotoirs = chantierServer.curer_depotoirs;
        this.nettoyerBords = chantierServer.nettoyer_bords;
        this.colmaterFissure = chantierServer.colmater_fissure;
        this.prTouches = chantierServer.pr_touches;
        this.autre = chantierServer.autre;
        this.lieuSeance = chantierServer.lieu_seance;
        this.jourSeance = chantierServer.jour_seance;
        this.heureSeance = chantierServer.heure_seance;
        this.reperageEffectif = chantierServer.reperage_effectif;
        this.categorie = [];
        if (categoriesChantier && categoriesChantier.length > 0) {
            categoriesChantier.forEach(cat => {
                this.categorie.push(cat.id);
            });
        }

        // this.categorie = chantierServer.cate
    }
}

export interface IChantierServerEdition {
    autre: string;
    boucle_induction: boolean;
    colmater_fissure: boolean;
    curer_depotoirs: boolean;
    epaisseur_caisson: string;
    epaisseur_revetement: string;
    epaisseur_support: string;
    faucher_accotement: boolean;
    heure_seance: string;
    id: number;
    id_centrale_enrobage: number;
    id_direction_locale: number;
    id_entrepreneur: number;
    id_evenement: number;
    id_maitre_ouvrage: number;
    id_responsable_travaux: number;
    jour_seance: string;
    lieu_seance: string;
    longueur_etape: number;
    nettoyer_bords: boolean;
    pr_touches: boolean;
    projet: string;
    qualite_caisson: string;
    qualite_encollage: string;
    qualite_revetement: string;
    qualite_support: string;
    surface: number;
    reperage_effectif: boolean;
}

export class ChantierServerSave extends EvenementServerForSave {
    _idMaitreOuvrage: number;
    _idDirectionLocale: number;
    _idEntrepreneur: number;
    _idResponsableTravaux: number;
    _projet: string;
    _longueurEtape: number;
    _surface: number;
    _idCentraleEnrobage: number;
    _epaisseurCaisson: string;
    _qualiteCaisson: string;
    _epaisseurSupport: string;
    _qualiteSupport: string;
    _epaisseurRevetement: string;
    _qualiteRevetement: string;
    _qualiteEncollage: string;
    _boucleInduction: string;
    _faucherAccotement: string;
    _curerDepotoirs: string;
    _nettoyer_bords: string;
    _colmater_fissure: string;
    _prTouches: string;
    _autre: string;
    _lieuSeance: string;
    _jourSeance: string;
    _heureSeance: string;
    _reperageEffectif: string;
    _categories: string;

    constructor(evenement: EvenementFormValues, geometries?: any[]) {
        super(evenement, geometries);
        const chantier = evenement.chantier;
        this._idMaitreOuvrage = chantier.maitreOuvrage;
        this._idDirectionLocale = chantier.directionLocale;
        this._idEntrepreneur = chantier.entrepreneur;
        this._idResponsableTravaux = chantier.responsableTravaux;
        this._projet = chantier.projet;
        this._longueurEtape = chantier.longueurEtape;
        this._surface = chantier.surface;
        this._idCentraleEnrobage = chantier.centraleEnrobage;
        this._epaisseurCaisson = chantier.epaisseurCaisson;
        this._qualiteCaisson = chantier.qualiteCaisson;
        this._epaisseurSupport = chantier.epaisseurSupport;
        this._qualiteSupport = chantier.qualiteSupport;
        this._epaisseurRevetement = chantier.epaisseurRevetement;
        this._qualiteRevetement = chantier.qualiteRevetement;
        this._qualiteEncollage = chantier.qualiteEncollage;
        this._boucleInduction = chantier.boucleInduction ? 'true' : 'false';
        this._faucherAccotement = chantier.faucherAccotement ? 'true' : 'false';
        this._curerDepotoirs = chantier.curerDepotoirs ? 'true' : 'false';
        this._nettoyer_bords = chantier.nettoyerBords ? 'true' : 'false';
        this._colmater_fissure = chantier.colmaterFissure ? 'true' : 'false';
        this._prTouches = chantier.prTouches ? 'true' : 'false';
        this._reperageEffectif = chantier.reperageEffectif ? 'true' : 'false';
        this._autre = chantier.autre;
        this._lieuSeance = chantier.lieuSeance;
        this._jourSeance = DateUtils.formatDate(chantier.jourSeance);
        this._heureSeance = chantier.heureSeance;
        if (evenement.chantier.categorie && evenement.chantier.categorie.length > 0) {
            this._categories = JSON.stringify(evenement.chantier.categorie);
        }
    }
}

export interface IChantier {
    maitreOuvrage: IOrganisme;
    directionLocale: IContact;
    entrepreneur: IOrganisme;
    responsableTravaux: IContact;
    projet: string;
    longueurEtape: string;
    surface: string;
    centraleEnrobage: IOrganisme;
    epaisseurCaisson: string;
    qualiteCaisson: string;
    epaisseurSupport: string;
    qualiteSupport: string;
    epaisseurRevetement: string;
    qualiteRevetement: string;
    qualiteEncollage: string;
    boucleInduction: boolean;
    faucherAccotement: boolean;
    curerDepotoirs: boolean;
    nettoyerBords: boolean;
    colmaterFissure: boolean;
    prTouches: boolean;
    autre: any;
    lieuSeance: string;
    jourSeance: string;
    heureSeance: any;
    categorie: any;
    reperageEffectif: boolean;
}



export interface ICategorieChantier {
    id: number;
    description: string;
}
