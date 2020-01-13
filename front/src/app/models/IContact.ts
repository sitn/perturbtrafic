import { FormControl, FormGroup, Validators } from '@angular/forms';

export interface IContact {
    id: number;
    id_organisme?: number;
    nom: string;
    prenom: string;
    nomComplet: string;
    nomCompletEtLogin: string;
    login?: string;
    mobile: string;
    telephone: string;
    fax: string;
    courriel: string;
}

export interface IContactPreavis {
    id?: number;
    id_contact: number;
    nom?: string;
    prenom?: string;
    nomComplet?: string;
    courriel?: string;
    organisme?: string;
    envoi_auto_occupation: boolean;
    envoi_auto_fermeture: boolean;
    checked?: boolean;
}

export class ContactPreavisServerSave {
    id: number;
    idEntite: number;
    idContact: number;
    envoiAutoOccupation: string;
    envoiAutoFermeture: string;

    constructor(contactPreavis: IContactPreavis) {
        this.id = contactPreavis.id;
        this.idContact = contactPreavis.id_contact;
        this.envoiAutoFermeture = contactPreavis.envoi_auto_fermeture ? 'true' : 'false';
        this.envoiAutoOccupation = contactPreavis.envoi_auto_occupation ? 'true' : 'false';
        this.idEntite = 1;
    }
}

export interface IContactAutorisation {
    id?: number;
    id_delegant: number;
    id_contact: number;
    nom?: string;
    prenom?: string;
    nomComplet?: string;
    courriel?: string;
    organisme?: string;
    autorisation_lecture: boolean;
    autorisation_modification: boolean;
    autorisation_suppression: boolean;
    checked?: boolean;
}

export class ContactAutorisationServerSave {
    idDelegation: number;
    idDelegataire: number;
    autorisationLecture: string;
    autorisationModification: string;
    autorisationSuppression: string;

    constructor(contactAutorisation: IContactAutorisation) {
        this.idDelegation = contactAutorisation.id;
        this.idDelegataire = contactAutorisation.id_contact;
        this.autorisationLecture = contactAutorisation.autorisation_lecture ? 'true' : 'false';
        this.autorisationModification = contactAutorisation.autorisation_modification ? 'true' : 'false';
        this.autorisationSuppression = contactAutorisation.autorisation_suppression ? 'true' : 'false';
    }
}

export interface IContactPreavisUrgence {
    id?: number;
    id_contact: number;
    nom?: string;
    prenom?: string;
    nomComplet?: string;
    courriel?: string;
    organisme?: string;
}

export interface IContactAvisPrTouche {
    id?: number;
    id_contact: number;
    nom?: string;
    prenom?: string;
    nomComplet?: string;
    courriel?: string;
    organisme?: string;
}


export class ContactServerSave {
    id?: number;
    nom: string;
    prenom: string;
    mobile: string;
    telephone: string;
    courriel: string;
    login: string;

    constructor(contact: IContact) {
        if (contact.id) {
            this.id = contact.id;
        }
        this.nom = contact.nom;
        this.prenom = contact.prenom;
        this.mobile = contact.mobile;
        this.telephone = contact.telephone;
        this.courriel = contact.courriel;
        this.login = contact.login;
    }

}

export class ContactFormGroup {

    contact = new FormControl();
    contactInfos = new FormGroup({
        nom: new FormControl(null, Validators.maxLength(50)),
        prenom: new FormControl(null, Validators.maxLength(50)),
        mobile: new FormControl(null, [Validators.maxLength(20),
        Validators.pattern(
            /^\+?((\/|\.|\s)?\d+)+$/
        )]
        ),
        telephone: new FormControl(null, [Validators.maxLength(20),
        Validators.pattern(
            /^\+?((\/|\.|\s)?\d+)+$/
        )]
        ),
        fax: new FormControl(null, [Validators.maxLength(20),
        Validators.pattern(
            /^\+?((\/|\.|\s)?\d+)+$/
        )]),
        courriel: new FormControl(null, Validators.maxLength(50)),
    });
}

export class ContactFormValues {

    contact: any;
    contactInfos: {
        nom: string;
        prenom: string;
        mobile: string;
        telephone: string;
        fax: string;
        courriel: string;
    };

    constructor(id?: number, nom?: string, prenom?: string, mobile?: string, telephone?: string, fax?: string, courriel?: string) {
        // this.contact = { id: id };
        this.contactInfos = {
            nom: nom,
            prenom: prenom,
            mobile: mobile,
            telephone: telephone,
            fax: fax,
            courriel: courriel
        };
    }
}



export class ContactEditionFormGroup {
    id = new FormControl();
    nom = new FormControl(null, Validators.required);
    prenom = new FormControl(null);
    mobile = new FormControl();
    telephone = new FormControl();
    fax = new FormControl();
    courriel = new FormControl();
    login = new FormControl();
}
