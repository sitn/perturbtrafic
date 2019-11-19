import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

import { AutreEvenementFormGroup, AutreEvenementFormValues } from './IAutreEvenement';
import { ChantierFormGroup, ChantierFormValues } from './IChantier';
import { IEvenementServerEdition } from './IEvenement';
import { FouilleFormGroup, FouilleFormValues } from './IFouilleEvenement';
import { ManifestationFormGroup, ManifestationFormValues } from './IManifestationsEvenement';
import { OrganismeFormGroup, OrganismeFormValues } from '../IOrganisme';
import { ContactFormGroup, ContactFormValues } from '../IContact';

export class EvenementForm {
    id = new FormControl();
    numeroDossier = new FormControl({ value: null, disabled: true }, Validators.maxLength(20));
    type = new FormGroup({
        type: new FormControl(null, Validators.required)
    });
    /* fouille?: FormGroup;
    chantier?: FormGroup;
    autre?: FormGroup; */
    fouille = new FormBuilder().group(
        new FouilleFormGroup()
    );
    chantier = new FormBuilder().group(
        new ChantierFormGroup()
    );
    autre = new FormBuilder().group(
        new AutreEvenementFormGroup()
    );
    manifestation = new FormBuilder().group(
        new ManifestationFormGroup()
    );
    division = new FormControl(null, Validators.maxLength(50));
    libelle = new FormControl(null, [Validators.required, Validators.maxLength(200)]);
    description = new FormControl(null, Validators.maxLength(500));
    prevision = new FormControl();
    dates = new FormGroup({
        dateDebut: new FormControl(new Date()),
        dateFin: new FormControl(new Date()),
        heureDebut: new FormControl(null, [
            Validators.required,
            Validators.pattern('^(0[0-9]|1[0-9]|2[0-3]|[0-9]):?[0-5][0-9]:?([0-5][0-9])?$')
        ]),
        heureFin: new FormControl(null, [
            Validators.required,
            Validators.pattern('^(0[0-9]|1[0-9]|2[0-3]|[0-9]):?[0-5][0-9]:?([0-5][0-9])?$')
        ])
    }, this.dateOrderValidator);
    dateDemande = new FormControl(new Date());
    dateOctroi = new FormControl();
    localisation = new FormControl(null, Validators.maxLength(100));
    responsable = new FormControl(null, Validators.required);
    requerant = new FormBuilder().group(
        new OrganismeFormGroup()
    );
    contact = new FormBuilder().group(
        new ContactFormGroup()
    );
    remarque = new FormControl();
    dateAjout = new FormControl({ value: null, disabled: true });
    utilisateurAjout = new FormControl({ value: null, disabled: true });
    dateModification = new FormControl({ value: null, disabled: true });
    utilisateurModification = new FormControl({ value: null, disabled: true });
    srbTouche = new FormControl();

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


export class EvenementFormValues {
    id?: number;
    numeroDossier: string;
    type: { type: number };
    fouille?: FouilleFormValues;
    manifestation: ManifestationFormValues;
    chantier?: ChantierFormValues;
    autre?: AutreEvenementFormValues;
    division: string;
    libelle: string;
    description: string;
    prevision: boolean;
    dates: {
        dateDebut: Date;
        dateFin: Date;
        heureDebut: string;
        heureFin: string;
    };
    dateDemande: Date;
    localisation: string;
    responsable: number;
    requerant: OrganismeFormValues;
    contact: ContactFormValues;
    remarque: string;
    dateOctroi: Date;
    dateAjout: Date;
    utilisateurAjout: string;
    dateModification: Date;
    utilisateurModification: string;
    srbTouche: string;

    constructor(evenementServer: IEvenementServerEdition) {
        const infoEvenement = evenementServer.evenement;
        this.id = infoEvenement.id;
        this.numeroDossier = infoEvenement.numero_dossier;
        this.type = { type: infoEvenement.type };
        // this.fouille = new FouilleFormValues(evenementServer);
        // this.chantier = null;
        // this.autre = null;
        // this.fouille = null;
        if (infoEvenement.type === 1) {
            evenementServer.autre = evenementServer.infos;
            this.autre = new AutreEvenementFormValues(evenementServer.autre);
        } else if (infoEvenement.type === 2) {
            evenementServer.chantier = evenementServer.infos;
            this.chantier = new ChantierFormValues(evenementServer.chantier, evenementServer.categories_chantiers);
        } else if (infoEvenement.type === 3) {
            evenementServer.fouille = evenementServer.infos;
            this.fouille = new FouilleFormValues(evenementServer.fouille, evenementServer.plans_types_fouille);
        } else if (infoEvenement.type === 4) {
            evenementServer.manifestation = evenementServer.infos;
            this.manifestation = new ManifestationFormValues(evenementServer.manifestation);
        }
        this.division = infoEvenement.division;
        this.libelle = infoEvenement.libelle;
        this.description = infoEvenement.description;
        this.prevision = infoEvenement.prevision;
        this.dates = {
            dateDebut: infoEvenement.date_debut ? new Date(infoEvenement.date_debut) : null,
            dateFin: infoEvenement.date_fin ? new Date(infoEvenement.date_fin) : null,
            heureDebut: infoEvenement.heure_debut,
            heureFin: infoEvenement.heure_fin
        };
        this.dateDemande = infoEvenement.date_demande ? new Date(infoEvenement.date_demande) : null;
        this.dateOctroi = infoEvenement.date_octroi ? new Date(infoEvenement.date_octroi) : null;
        this.localisation = infoEvenement.localisation;
        this.responsable = infoEvenement.id_responsable;
        this.requerant = new OrganismeFormValues(
            infoEvenement.id_requerant,
            infoEvenement.nom_requerant,
            infoEvenement.rue_requerant,
            infoEvenement.localite_requerant,
            infoEvenement.telephone_requerant,
            infoEvenement.fax_requerant,
            infoEvenement.courriel_requerant
        );
        this.contact = new ContactFormValues(
            null,
            infoEvenement.nom_contact,
            infoEvenement.prenom_contact,
            infoEvenement.mobile_contact,
            infoEvenement.telephone_contact,
            infoEvenement.fax_contact,
            infoEvenement.courriel_contact
        );

        this.remarque = infoEvenement.remarque;
        this.dateAjout = infoEvenement.date_ajout ? new Date(infoEvenement.date_ajout) : null;
        this.utilisateurAjout = infoEvenement.nom_utilisateur_ajout;
        this.dateModification = infoEvenement.date_modification ? new Date(infoEvenement.date_modification) : null;
        this.utilisateurModification = infoEvenement.nom_utilisateur_modification;
        // this.srbTouche = evenementServer.tou;
    }
}
