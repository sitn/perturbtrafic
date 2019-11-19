import { FormControl, Validators } from '@angular/forms';

import { IPerturbationOccupationServerEdition, PerturbationFormValues } from './IPerturbation';
import { PerturbationServerForSave } from './PerturbationServer';

export class OccupationPerturbationFormGroup {
    typeOccupation = new FormControl(null, Validators.maxLength(50));
    typeRegulation = new FormControl(null, Validators.maxLength(50));
    voiesCondamnees = new FormControl(null, Validators.maxLength(50));
    largeurGabarit = new FormControl(null, Validators.maxLength(20));
    hauteurGabarit = new FormControl(null, Validators.maxLength(20));
    heurePointe = new FormControl();
    weekend = new FormControl();
    responsable = new FormControl();
}

export class OccupationFormValues {
    typeOccupation: string[];
    typeRegulation: string;
    voiesCondamnees: string;
    largeurGabarit: string;
    hauteurGabarit: string;
    heurePointe: boolean;
    weekend: boolean;
    responsable: number;

    constructor(occupation: IPerturbationOccupationServerEdition) {
        this.typeOccupation = [];
        if (occupation) {

            if (occupation && occupation.type_occupation && occupation.type_occupation.length > 0) {
                this.typeOccupation = occupation.type_occupation.split(',');
            }
            this.typeRegulation = occupation.type_regulation;
            this.voiesCondamnees = occupation.voies_condamnees;
            this.largeurGabarit = occupation.largeur_gabarit;
            this.hauteurGabarit = occupation.hauteur_gabarit;
            this.heurePointe = occupation.heure_pointe;
            this.weekend = occupation.week_end;
            this.responsable = occupation.id_responsable_regulation;
        }
    }
}

export class OccupationServerSave extends PerturbationServerForSave {
    _idResponsableRegulation: number;
    _typeOccupation: string;
    _typeRegulation: string;
    _voiesCondamnees: string;
    _largeurGabarit: string;
    _hauteurGabarit: string;
    _heurePointe: string;
    _weekEnd: string;

    constructor(perturbationValue: PerturbationFormValues, geometries?: any[], contacts?: number[]) {
        super(perturbationValue, geometries, [], contacts);

        const occupationValue = perturbationValue.occupation;
        this._idResponsableRegulation = occupationValue.responsable;
        if (occupationValue.typeOccupation && occupationValue.typeOccupation.length > 0) {
            this._typeOccupation = occupationValue.typeOccupation.join(',');
        }
        this._typeRegulation = occupationValue.typeRegulation;
        this._voiesCondamnees = occupationValue.voiesCondamnees;
        this._largeurGabarit = occupationValue.largeurGabarit;
        this._hauteurGabarit = occupationValue.hauteurGabarit;
        this._heurePointe = occupationValue.heurePointe ? 'true' : 'false';
        this._weekEnd = occupationValue.weekend ? 'true' : 'false';
    }
}
