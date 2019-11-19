import { Injectable } from '@angular/core';

@Injectable()
export class InputsUtils {

    constructor() { }

    initiateKendoDropDownList(): any {
        return [{ id: null, description: '-' }];
    }
}
