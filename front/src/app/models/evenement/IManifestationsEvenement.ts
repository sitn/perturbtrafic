import { FormControl, Validators } from '@angular/forms';
import { EvenementServerForSave } from './EvenementServer';
import { EvenementFormValues } from './IEvenementForm';
import { IUser } from '../IUser';

export class ManifestationFormGroup {
    parcours = new FormControl(null, Validators.maxLength(2048));
}

export class ManifestationFormValues {
    parcours: string;
    constructor(manifestation: ManifestationServerEdition) {
        this.parcours = manifestation.parcours;
    }
}

export class ManifestationServerEdition {
    parcours: string;
}

export class ManifestationServerSave extends EvenementServerForSave {
    _parcours: string;

    constructor(evenement: EvenementFormValues, user: IUser, geometries?: any[]) {
        super(evenement, user, geometries);
        const manifestationValues = evenement.manifestation;
        this._parcours = manifestationValues.parcours;
    }
}
