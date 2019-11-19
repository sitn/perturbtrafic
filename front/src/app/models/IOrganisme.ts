import { FormControl, FormGroup, Validators } from '@angular/forms';

export interface IOrganisme {
    id: any;
    nom: string;
    adresse: string;
    localite: any;
    telephone: string;
    fax: string;
    courriel: string;
}

export class OrganismeServerSave {
    id?: number;
    nom: string;
    adresse: string;
    localite: string;
    telephone: string;
    fax: string;
    courriel: string;

    constructor(organisme: IOrganisme) {
        if (organisme.id) {
            this.id = organisme.id;
        }
        this.nom = organisme.nom;
        this.adresse = organisme.adresse;
        this.localite = organisme.localite;
        this.telephone = organisme.telephone;
        this.courriel = organisme.courriel;
        this.fax = organisme.fax;
    }

}

export class OrganismeFormGroup {

    organisme = new FormControl();
    contactInfos = new FormGroup({
        nom: new FormControl(null, Validators.maxLength(50)),
        adresse: new FormControl(null, Validators.maxLength(100)),
        localite: new FormControl(null, Validators.maxLength(50)),
        telephone: new FormControl(null, [Validators.maxLength(20),
        Validators.pattern(
            /^\+?((\/|\.|\s)?\d+)+$/
        )]
        ),
        fax: new FormControl(null, [Validators.maxLength(20),
        Validators.pattern(
            /^\+?((\/|\.|\s)?\d+)+$/
        )]),
        courriel: new FormControl(null, Validators.maxLength(50))
    });
}

export class OrganismeFormValues {
    organisme: any;
    contactInfos: {
        nom: string;
        adresse: string;
        localite: string;
        telephone: string;
        fax: string;
        courriel: string;
    };

    constructor(id?: number, nom?: string, adresse?: string, localite?: string, telephone?: string, fax?: string, courriel?: string) {
        // this.organisme = { id: id };
        this.contactInfos = <any>{};
        this.contactInfos.nom = nom;
        this.contactInfos.adresse = adresse;
        this.contactInfos.localite = localite;
        this.contactInfos.telephone = telephone;
        this.contactInfos.fax = fax;
        this.contactInfos.courriel = courriel;
    }
}

export class OrganismeEditionFormGroup {
    id = new FormControl();
    nom = new FormControl(null, Validators.required);
    adresse = new FormControl();
    localite = new FormControl();
    telephone = new FormControl(null, [Validators.maxLength(20),
    Validators.pattern(
        /^\+?((\/|\.|\s)?\d+)+$/
    )]
    );
    fax = new FormControl(null, [Validators.maxLength(20),
    Validators.pattern(
        /^\+?((\/|\.|\s)?\d+)+$/
    )]);
    courriel = new FormControl();
}
