import { FormControl } from '@angular/forms';

import { IPerturbationFermetureServerEdition, PerturbationFormValues } from './IPerturbation';
import { PerturbationServerForSave } from './PerturbationServer';

export interface IFermeture {
    responsable: number;
    deviation: string;
}

export class FermeturePerturbationFormGroup {
    deviation = new FormControl();
    responsable = new FormControl();
}

export class FermetureFormValues {
    responsable: number;
    deviation: string;

    constructor(fermeture: IPerturbationFermetureServerEdition) {
        if (fermeture) {
            this.responsable = fermeture.id_responsable;
            this.deviation = fermeture.deviation;
        }
    }
}

export class FermetureServerEdition {
    id?: number;
    id_perturbation?: number;
    id_responsable: number;
    deviation: string;
}

export class FermetureServerSave extends PerturbationServerForSave {
    _deviation: string;
    _idResponsable: number;

    constructor(perturbationValue: PerturbationFormValues, geometries?: any[], deviations?: any[], contacts?: number[]) {
        super(perturbationValue, geometries, deviations, contacts);

        const fermetureValue = perturbationValue.fermeture;
        this._deviation = fermetureValue.deviation;
        this._idResponsable = fermetureValue.responsable;
    }
}
