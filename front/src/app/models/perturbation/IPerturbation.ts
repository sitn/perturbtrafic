import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

import { ContactFormGroup, ContactFormValues, IContact } from '../IContact';
import { IReperageServer } from '../IReperage';
import { FermetureFormValues, FermeturePerturbationFormGroup } from './IFermeturePerturbation';
import { OccupationFormValues, OccupationPerturbationFormGroup } from './IOccupationPerturbation';

export interface IPerturbation {
    type: IPerturbationType;
    description: string;
    localisation: string;
    dateDebut: Date;
    heureDebut: any;
    dateFin: Date;
    heureFin: any;
    trancheHoraire: boolean;
    responsableTrafic: IContact;
    remarque: string;
    urgence: boolean;
    etat: string;
    utilisateurValidation: string;
    dateValidation: Date;
    dateDecision: Date;
    decision: string;
}

export class Perturbation implements IPerturbation {
    type: IPerturbationType;
    description: string;
    localisation: string;
    dateDebut: Date;
    heureDebut: any;
    dateFin: Date;
    heureFin: any;
    trancheHoraire: boolean;
    responsableTrafic: IContact;
    remarque: string;
    urgence: boolean;
    etat: string;
    utilisateurValidation: string;
    dateValidation: Date;
    dateDecision: Date;
    decision: string;

    constructor(perturbationForm: PerturbationForm) {
        this.type = perturbationForm.type.value;
        this.description = perturbationForm.description.value;
        this.localisation = perturbationForm.localisation.value;
        this.dateDebut = perturbationForm.dates.controls.dateDebut.value;
        // this.heureDebut = perturbationForm..controls.heureDebut.value;
        this.dateFin = perturbationForm.description.value;
        this.heureFin = perturbationForm.description.value;
        this.trancheHoraire = perturbationForm.description.value;
        this.responsableTrafic = perturbationForm.description.value;
        this.remarque = perturbationForm.description.value;
        this.urgence = perturbationForm.description.value;
        this.etat = perturbationForm.description.value;
        this.utilisateurValidation = perturbationForm.description.value;
        this.dateValidation = perturbationForm.description.value;
        this.dateDecision = perturbationForm.description.value;
        this.decision = perturbationForm.description.value;
    }
}

export class PerturbationForm {

    id = new FormControl();
    type = new FormControl(null, Validators.required);
    evenement = new FormGroup({
        type: new FormControl(null),
        evenement: new FormControl(null, Validators.required)
    });
    dates = new FormGroup({
        dateDebut: new FormControl(null, Validators.required),
        dateFin: new FormControl(null, Validators.required),
        heureDebut: new FormControl(null, [
            Validators.required,
            Validators.pattern('^(0[0-9]|1[0-9]|2[0-3]|[0-9]):?[0-5][0-9]:?([0-5][0-9])?$')
        ]),
        heureFin: new FormControl(null, [
            Validators.required,
            Validators.pattern('^(0[0-9]|1[0-9]|2[0-3]|[0-9]):?[0-5][0-9]:?([0-5][0-9])?$')
        ])
    }, this.dateOrderValidator);
    description = new FormControl(null, Validators.maxLength(200));
    localisation = new FormControl(null, Validators.maxLength(100));
    trancheHoraire = new FormControl();
    responsableTrafic = new FormBuilder().group(
        new ContactFormGroup()
    );
    remarque = new FormControl();
    urgence = new FormControl();
    etat = new FormControl({ disabled: true });
    utilisateurValidation = new FormControl({ disabled: true }, Validators.maxLength(20));
    dateValidation = new FormControl({ disabled: true });
    dateDecision = new FormControl({ disabled: true });
    decision = new FormControl({ disabled: true }, Validators.maxLength(200));
    fermeture = new FormBuilder().group(
        new FermeturePerturbationFormGroup()
    );
    occupation = new FormBuilder().group(
        new OccupationPerturbationFormGroup()
    );

    utilisateurAjout = new FormControl({ disabled: true });
    dateAjout = new FormControl({ disabled: true });
    utilisateurModification = new FormControl({ disabled: true });
    dateModification = new FormControl({ disabled: true });

    private dateOrderValidator(g: FormGroup) {
        const valueDebut = g.get('dateDebut').value;
        const valueFin: any = g.get('dateFin');
        const valueFinValue = g.get('dateFin').value;



        if (valueDebut && valueFinValue) {
            const debut = new Date(valueDebut);
            const fin = new Date(valueFinValue);

            if (debut > fin) {
                valueFin.setErrors({ 'invalid: ': true });
                return { 'invalidDates': { value: 'pb dates' } };
            } else {
                return null;
            }
        } else {
            if (!valueDebut) {
                g.get('dateDebut').setErrors({ 'required: ': true });
                return { 'invalidDates': { value: 'pb dates' } };
            }
            if (!valueFinValue) {
                valueFin.setErrors({ 'required: ': true });
                return { 'invalidDates': { value: 'pb dates' } };
            }
        }

    }

}

export class PerturbationFormValues {
    id?: number;
    type: number;
    evenement: {
        type: number,
        evenement: number
    };
    fermeture?: FermetureFormValues;
    occupation?: OccupationFormValues;
    dates: {
        dateDebut: Date;
        dateFin: Date;
        heureDebut: string;
        heureFin: string;
    };
    description: string;
    localisation: string;
    trancheHoraire: boolean;
    responsableTrafic: ContactFormValues;
    remarque: string;
    urgence: boolean;
    etat: number;
    utilisateurValidation: string;
    dateValidation: Date;
    dateDecision: Date;
    decision: string;
    dateAjout: Date;
    utilisateurAjout: string;
    dateModification: Date;
    utilisateurModification: string;

    constructor(perturbationServer: IPerturbationServerEdition, cloned = false) {
        this.id = perturbationServer.perturbation.id;
        this.type = perturbationServer.perturbation.type;
        this.evenement = {
            type: 1, // perturbation.e, // TODO
            evenement: perturbationServer.perturbation.id_evenement
        };
        if (perturbationServer.perturbation.type === 1) {
            this.fermeture = new FermetureFormValues(perturbationServer.infos);
        } else if (perturbationServer.perturbation.type === 2) {
            this.occupation = new OccupationFormValues(perturbationServer.infos);
        }
        this.dates = {
            dateDebut: perturbationServer.perturbation.date_debut ? new Date(perturbationServer.perturbation.date_debut) : null,
            dateFin: perturbationServer.perturbation.date_fin ? new Date(perturbationServer.perturbation.date_fin) : null,
            heureDebut: perturbationServer.perturbation.heure_debut,
            heureFin: perturbationServer.perturbation.heure_fin
        };
        this.description = perturbationServer.perturbation.description;
        this.localisation = perturbationServer.perturbation.localisation;
        this.trancheHoraire = perturbationServer.perturbation.tranche_horaire;
        this.responsableTrafic = new ContactFormValues(
            null,
            perturbationServer.perturbation.nom_responsable_trafic,
            perturbationServer.perturbation.prenom_responsable_trafic,
            perturbationServer.perturbation.mobile_responsable_trafic,
            perturbationServer.perturbation.telephone_responsable_trafic,
            perturbationServer.perturbation.fax_responsable_trafic,
            perturbationServer.perturbation.courriel_responsable_trafic);
        this.remarque = perturbationServer.perturbation.remarque;
        this.urgence = perturbationServer.perturbation.urgence;
        this.etat = cloned ? null : perturbationServer.perturbation.etat;
        this.utilisateurValidation = cloned ? null : perturbationServer.perturbation.nom_utilisateur_validation;
        this.utilisateurAjout = cloned ? null : perturbationServer.perturbation.nom_utilisateur_ajout;
        this.utilisateurModification = cloned ? null : perturbationServer.perturbation.nom_utilisateur_modification;
        this.dateAjout = cloned ? null :
            perturbationServer.perturbation.date_ajout ? new Date(perturbationServer.perturbation.date_ajout) : null;
        this.dateModification = cloned ? null :
            perturbationServer.perturbation.date_modification ? new Date(perturbationServer.perturbation.date_modification) : null;
        this.dateValidation = cloned ? null :
            perturbationServer.perturbation.date_validation ? new Date(perturbationServer.perturbation.date_validation) : null;
        this.dateDecision = cloned ? null :
            perturbationServer.perturbation.date_decision ? new Date(perturbationServer.perturbation.date_decision) : null;
        this.decision = cloned ? null : perturbationServer.perturbation.decision;
    }
}

export interface IPerturbationPerturbationServerEdition {
    courriel_responsable_trafic: string;
    date_ajout: string;
    date_debut: string;
    date_decision: string;
    date_fin: string;
    date_modification: string;
    date_suppression: string;
    date_validation: string;
    decision: string;
    description: string;
    etat: number;
    fax_responsable_trafic: string;
    heure_debut: string;
    heure_fin: string;
    id: number;
    id_evenement: number;
    id_responsable_trafic: number;
    id_utilisateur_ajout: number;
    nom_utilisateur_ajout: string;
    id_utilisateur_modification: number;
    nom_utilisateur_modification: string;
    localisation: string;
    mobile_responsable_trafic: string;
    nom_responsable_trafic: string;
    prenom_responsable_trafic: string;
    remarque: string;
    telephone_responsable_trafic: string;
    tranche_horaire: boolean;
    type: number;
    urgence: boolean;
    nom_utilisateur_validation: string;
}

export interface IPerturbationFermetureServerEdition {
    deviation: string;
    id: number;
    id_perturbation: number;
    id_responsable: number;
}

export interface IPerturbationOccupationServerEdition {
    hauteur_gabarit: string;
    heure_pointe: boolean;
    id: number;
    id_perturbation: number;
    id_responsable_regulation: number;
    largeur_gabarit: string;
    type_occupation: string;
    type_regulation: string;
    voies_condamnees: string;
    week_end: boolean;
}

export interface IPerturbationServerEdition {
    perturbation: IPerturbationPerturbationServerEdition;
    infos: any;
    geometries: any[];
    deviations: any[];
    contacts_a_aviser: IContact[];
    reperages?: IReperageServer[];
}

export interface IPerturbationType {
    id: number;
    description: string;
}

export interface IPerturbationEtat {
    id: number;
    description: string;
}


export interface IPerturbationImpression {
    id: number;
    type: number;
    type_description: string;
    urgence: boolean;
    numero_dossier: string;
    libelle_evenement: string;
    type_description_evenement: string;
    description: string;
    decision: string;
    deviation: string;
    division?: string;
    etat_description: string;
    date_debut: string;
    heure_debut: string;
    date_fin: string;
    heure_fin: string;
    courriel_responsable_trafic: string;
    nom_responsable_trafic: string;
    prenom_responsable_trafic: string;
    mobile_responsable_trafic: string;
    fax_responsable_trafic: string;
    telephone_responsable_trafic: string;
    tranche_horaire: boolean;
    localisation: string;
    remarque: string;
    nom_entite: string;
    type_occupation: string;
    voies_condamnees: string;
    type_regulation: string;
    largeur_gabarit: string;
    hauteur_gabarit: string;
    heure_pointe: boolean;
    week_end: boolean;
    geometry_point: any;
    geometry_ligne: any;
    geometry_polygone: any;
    preavis_contacts: {
        date_envoi: any;
        nom: string;
        prenom: string;
    };
    reperages: any;
    canvas?: any;
}

