import { IContact } from '../IContact';
import { IOrganisme } from '../IOrganisme';
import { EvenementServer } from './EvenementServer';
import { AutreEvenementServerEdition } from './IAutreEvenement';
import { IChantierServerEdition } from './IChantier';
import { FouilleServerEdition, IFouille } from './IFouilleEvenement';
import { ManifestationServerEdition } from './IManifestationsEvenement';
import { IReperageServer } from '../IReperage';



export interface IEvenementType {
    id: number;
    description: string;
}

export interface IEvenementLibelle {
    id: number;
    libelle: string;
    numero_dossier: string;
    description: string;
    label?: string;
}

export interface IEvenementServerEdition {
    evenement: EvenementServer;
    infos: any;
    categories_chantiers?: any;
    plans_types_fouille?: any;
    chantier?: IChantierServerEdition;
    autre?: AutreEvenementServerEdition;
    fouille?: FouilleServerEdition;
    manifestation?: ManifestationServerEdition;
    geometries?: any;
    deviations?: any;
    reperages?: IReperageServer[];
}

export interface IEvenement {
    type: IEvenementType;
    fouille?: IFouille;
    numeroDossier: string;
    division: string;
    libelle: string;
    description: string;
    prevision: boolean;
    dateDebut: Date;
    heureDebut: any;
    dateFin: Date;
    heureFin: any;
    dateDemande: Date;
    localisation: string;
    responsable: any;
    requerant: IOrganisme;
    contact: IContact;
    remarque: string;
    dateOctroi: Date;
    dateAjout: Date;
    utilisateurAjout: any;
    dateModification: Date;
    utilisateurModification: any;
}


export interface IEvenementImpression {
    canvas?: any;
    date_debut: string;
    date_demande: string;
    date_facture: string;
    date_fin: string;
    division: string;
    geometry_ligne: any[];
    geometry_point: any[];
    geometry_polygone: any[];
    heure_debut: string;
    heure_fin: string;
    id: number;
    libelle: string;
    localisation: string;
    localisation_impression: string;
    localisationImpressionReperage?: {
        id_evenement: string;
        axe: string;
        pr_debut: string;
        pr_debut_distance: string;
        pr_fin: string;
        pr_fin_distance: string;
    }[];
    mobile_direction_locale: string;
    mobile_responsable: string;
    mobile_responsable_travaux: string;
    nom_direction_locale: string;
    nom_entrepreneur: string;
    nom_entite: string;
    logo_entite: string;
    nom_maitre_ouvrage: string;
    nom_requerant: string;
    nom_responsable: string;
    nom_responsable_travaux: string;
    numero_dossier: string;
    prenom_direction_locale: string;
    prenom_responsable: string;
    prenom_responsable_travaux: string;
    prevision: string;
    type: number;
    type_description: string;
}
